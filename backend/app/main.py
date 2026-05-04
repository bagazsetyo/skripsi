from __future__ import annotations

from io import BytesIO
from pathlib import Path

from fastapi import BackgroundTasks, Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch

from app.auth import authenticate_admin, create_access_token, get_current_admin
from app.inference import Predictor
from app.schemas import LoginRequest, LoginResponse, PredictionResponse, TrainingRequest
from config import CLASS_NAMES, CORS_ALLOW_ORIGINS, SCORE_THRESHOLD
from dataset_scan import build_class_lookup, scan_dataset, validate_dataset
from db import (
    get_active_model,
    get_dataset_cache,
    get_training_run,
    init_db,
    list_models,
    list_training_runs,
    utc_now,
    upsert_dataset_cache,
)
from model_registry import activate_model, ensure_default_model_registered, get_model_or_none, resolve_active_model_path
from training_service import (
    create_training_run_record,
    execute_training_run,
    materialize_training_request,
)

app = FastAPI(title="Traffic Sign Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor: Predictor | None = None
active_model_cache: dict | None = None
dataset_refresh_state = {
    "is_refreshing": False,
    "last_started_at": None,
    "last_completed_at": None,
    "last_error": None,
}


def _device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def reload_active_predictor() -> None:
    global predictor, active_model_cache
    active_model, model_path = resolve_active_model_path()
    active_model_cache = active_model
    if active_model is None or model_path is None:
        predictor = None
        return

    predictor = Predictor(model_path, active_model["class_names"] or CLASS_NAMES, _device())


def refresh_dataset_cache() -> dict:
    summary = scan_dataset()
    validation = validate_dataset()
    summary_cache = upsert_dataset_cache("summary", summary)
    validation_cache = upsert_dataset_cache("validation", validation)
    return {
        "summary": summary_cache["payload"],
        "validation": validation_cache["payload"],
        "updated_at": max(summary_cache["updated_at"], validation_cache["updated_at"]),
    }


def run_dataset_refresh_job() -> None:
    dataset_refresh_state["is_refreshing"] = True
    dataset_refresh_state["last_started_at"] = utc_now()
    dataset_refresh_state["last_error"] = None

    try:
        refresh_dataset_cache()
        dataset_refresh_state["last_completed_at"] = utc_now()
    except Exception as exc:
        dataset_refresh_state["last_error"] = str(exc)
    finally:
        dataset_refresh_state["is_refreshing"] = False


def get_dataset_cache_payload(cache_key: str, *, refresh_if_missing: bool = True) -> dict:
    cached = get_dataset_cache(cache_key)
    if cached is not None:
        return cached["payload"]

    if refresh_if_missing:
        refresh_dataset_cache()
        cached = get_dataset_cache(cache_key)
        if cached is not None:
            return cached["payload"]

    raise HTTPException(status_code=500, detail=f"Dataset cache '{cache_key}' is not available")


def run_training_job(run_id: int, request: TrainingRequest) -> None:
    model_record = execute_training_run(run_id, request)
    if model_record is not None and model_record["is_active"]:
        reload_active_predictor()


@app.on_event("startup")
def startup() -> None:
    init_db()
    ensure_default_model_registered()
    reload_active_predictor()
    refresh_dataset_cache()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": predictor is not None,
        "active_model": active_model_cache["version"] if active_model_cache else None,
    }


@app.post("/auth/login", response_model=LoginResponse)
def auth_login(request: LoginRequest):
    admin = authenticate_admin(request.username, request.password)
    if admin is None:
        raise HTTPException(status_code=401, detail="Username atau password salah")

    token = create_access_token(admin)
    return LoginResponse(
        access_token=token,
        username=admin["username"],
        role=admin["role"],
    )


@app.get("/auth/me")
def auth_me(current_admin: dict = Depends(get_current_admin)):
    return current_admin


@app.get("/dataset/classes")
def dataset_classes(_: dict = Depends(get_current_admin)):
    return build_class_lookup()


@app.get("/dataset/summary")
def dataset_summary(_: dict = Depends(get_current_admin)):
    return get_dataset_cache_payload("summary")


@app.get("/dataset/validation")
def dataset_validation(_: dict = Depends(get_current_admin)):
    return get_dataset_cache_payload("validation")


@app.post("/dataset/refresh")
def dataset_refresh(background_tasks: BackgroundTasks, _: dict = Depends(get_current_admin)):
    if dataset_refresh_state["is_refreshing"]:
        return {
            "status": "running",
            "message": "Dataset refresh is already running in the background.",
            "last_started_at": dataset_refresh_state["last_started_at"],
        }

    background_tasks.add_task(run_dataset_refresh_job)
    return {
        "status": "queued",
        "message": "Dataset refresh has started in the background.",
    }


@app.get("/training/config")
def training_config(_: dict = Depends(get_current_admin)):
    return {
        "selection_modes": ["all", "subset"],
        "available_classes": build_class_lookup(),
        "defaults": TrainingRequest(run_name="default-run").model_dump(),
    }


@app.post("/training/runs")
def create_training_run(
    request: TrainingRequest,
    background_tasks: BackgroundTasks,
    _: dict = Depends(get_current_admin),
):
    request = materialize_training_request(request)
    run_record = create_training_run_record(request)
    background_tasks.add_task(run_training_job, run_record["id"], request)
    return run_record


@app.get("/training/runs")
def training_runs(_: dict = Depends(get_current_admin)):
    return list_training_runs()


@app.get("/training/runs/{run_id}")
def training_run_detail(run_id: int, _: dict = Depends(get_current_admin)):
    run_record = get_training_run(run_id)
    if run_record is None:
        raise HTTPException(status_code=404, detail="Training run not found")
    return run_record


@app.get("/models")
def models(_: dict = Depends(get_current_admin)):
    return list_models()


@app.get("/models/active")
def active_model():
    model = get_active_model()
    if model is None:
        raise HTTPException(status_code=404, detail="No active model found")
    return model


@app.post("/models/{model_id}/activate")
def activate_model_endpoint(model_id: int, _: dict = Depends(get_current_admin)):
    model = get_model_or_none(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    if not Path(model["path"]).exists():
        raise HTTPException(status_code=400, detail="Model path does not exist")
    activated = activate_model(model_id)
    reload_active_predictor()
    return activated


@app.get("/models/{model_id}/evaluation")
def model_evaluation(model_id: int, _: dict = Depends(get_current_admin)):
    model = get_model_or_none(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return {
        "model_id": model["id"],
        "version": model["version"],
        "display_name": model["display_name"],
        "metrics": model["metrics"],
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...), score_threshold: float = SCORE_THRESHOLD):
    if predictor is None or active_model_cache is None:
        raise HTTPException(status_code=503, detail="No active model is loaded")
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()
    try:
        image = Image.open(BytesIO(contents)).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid image file") from exc

    results = predictor.predict(image, score_threshold=score_threshold)
    return PredictionResponse(
        model_id=active_model_cache["id"],
        model_version=active_model_cache["version"],
        model_display_name=active_model_cache["display_name"],
        score_threshold=score_threshold,
        image_width=image.width,
        image_height=image.height,
        detections=results,
    )
