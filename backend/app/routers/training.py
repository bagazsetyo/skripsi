from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

import app.state as state
from app.auth import get_current_admin
from app.schemas import TrainingRequest
from core.db import get_training_run, list_training_runs
from services.dataset_scan import build_class_lookup
from services.training_service import create_training_run_record, materialize_training_request

router = APIRouter(prefix="/training", tags=["training"])


@router.get("/config")
def training_config(_: dict = Depends(get_current_admin)):
    return {
        "selection_modes": ["all", "subset"],
        "available_classes": build_class_lookup(),
        "defaults": TrainingRequest(run_name="default-run").model_dump(),
    }


@router.post("/runs")
def create_training_run(
    request: TrainingRequest,
    background_tasks: BackgroundTasks,
    _: dict = Depends(get_current_admin),
):
    request = materialize_training_request(request)
    run_record = create_training_run_record(request)
    background_tasks.add_task(state.run_training_job, run_record["id"], request)
    return run_record


@router.get("/runs")
def training_runs(_: dict = Depends(get_current_admin)):
    return list_training_runs()


@router.get("/runs/{run_id}")
def training_run_detail(run_id: int, _: dict = Depends(get_current_admin)):
    run_record = get_training_run(run_id)
    if run_record is None:
        raise HTTPException(status_code=404, detail="Training run not found")
    return run_record
