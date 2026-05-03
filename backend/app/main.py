from __future__ import annotations

from io import BytesIO
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch

from app.inference import Predictor
from app.schemas import PredictionResponse, TrainingRequest
from config import CLASS_NAMES, CORS_ALLOW_ORIGINS, SCORE_THRESHOLD
from dataset_scan import build_class_lookup, scan_dataset, validate_dataset
from db import get_active_model, get_training_run, init_db, list_models, list_training_runs
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


def run_training_job(run_id: int, request: TrainingRequest) -> None:
    model_record = execute_training_run(run_id, request)
    if model_record is not None and model_record["is_active"]:
        reload_active_predictor()


@app.on_event("startup")
def startup() -> None:
    init_db()
    ensure_default_model_registered()
    reload_active_predictor()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": predictor is not None,
        "active_model": active_model_cache["version"] if active_model_cache else None,
    }


@app.get("/dataset/classes")
def dataset_classes():
    return build_class_lookup()


@app.get("/dataset/summary")
def dataset_summary():
    return scan_dataset()


@app.get("/dataset/validation")
def dataset_validation():
    return validate_dataset()


@app.get("/training/config")
def training_config():
    return {
        "selection_modes": ["all", "subset"],
        "available_classes": build_class_lookup(),
        "defaults": TrainingRequest(run_name="default-run").model_dump(),
    }


@app.post("/training/runs")
def create_training_run(request: TrainingRequest, background_tasks: BackgroundTasks):
    request = materialize_training_request(request)
    run_record = create_training_run_record(request)
    background_tasks.add_task(run_training_job, run_record["id"], request)
    return run_record


@app.get("/training/runs")
def training_runs():
    return list_training_runs()


@app.get("/training/runs/{run_id}")
def training_run_detail(run_id: int):
    run_record = get_training_run(run_id)
    if run_record is None:
        raise HTTPException(status_code=404, detail="Training run not found")
    return run_record


@app.get("/models")
def models():
    return list_models()


@app.get("/models/active")
def active_model():
    model = get_active_model()
    if model is None:
        raise HTTPException(status_code=404, detail="No active model found")
    return model


@app.post("/models/{model_id}/activate")
def activate_model_endpoint(model_id: int):
    model = get_model_or_none(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    if not Path(model["path"]).exists():
        raise HTTPException(status_code=400, detail="Model path does not exist")
    activated = activate_model(model_id)
    reload_active_predictor()
    return activated


@app.get("/models/{model_id}/evaluation")
def model_evaluation(model_id: int):
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
