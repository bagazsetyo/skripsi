from __future__ import annotations

import torch
from fastapi import HTTPException

from app.inference import Predictor
from core.config import CLASS_NAMES
from core.db import get_dataset_cache, upsert_dataset_cache, utc_now
from services.dataset_scan import scan_dataset, validate_dataset
from services.model_registry import resolve_active_model_path
from services.training_service import execute_training_run

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


def run_training_job(run_id: int, request) -> None:
    model_record = execute_training_run(run_id, request)
    if model_record is not None and model_record["is_active"]:
        reload_active_predictor()
