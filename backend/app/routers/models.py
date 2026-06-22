from __future__ import annotations

import os
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

import app.state as state
from app.auth import get_current_admin
from core.db import get_active_model, list_models
from services.model_import import import_model_archive
from services.model_registry import activate_model, get_model_or_none

router = APIRouter(prefix="/models", tags=["models"])


@router.get("")
def models(_: dict = Depends(get_current_admin)):
    return list_models()


@router.post("/import")
async def import_model_endpoint(
    file: UploadFile = File(...),
    display_name: str | None = Form(default=None),
    version: str | None = Form(default=None),
    activate_after_import: bool = Form(default=False),
    _: dict = Depends(get_current_admin),
):
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Imported model must be a .zip archive")

    temp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_file:
            temp_path = temp_file.name
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                temp_file.write(chunk)

        model_record = import_model_archive(
            Path(temp_path),
            display_name=display_name,
            version=version,
            activate=activate_after_import,
        )
        if model_record["is_active"]:
            state.reload_active_predictor()
        return model_record
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await file.close()
        if temp_path and Path(temp_path).exists():
            os.unlink(temp_path)


@router.get("/active")
def active_model():
    model = get_active_model()
    if model is None:
        raise HTTPException(status_code=404, detail="No active model found")
    return model


@router.post("/{model_id}/activate")
def activate_model_endpoint(model_id: int, _: dict = Depends(get_current_admin)):
    model = get_model_or_none(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    if not Path(model["path"]).exists():
        raise HTTPException(status_code=400, detail="Model path does not exist")
    activated = activate_model(model_id)
    state.reload_active_predictor()
    return activated


@router.get("/{model_id}/evaluation")
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
