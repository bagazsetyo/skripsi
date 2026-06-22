from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.state as state
from app.routers import auth, dataset, models, predict, tools, training
from core.config import CORS_ALLOW_ORIGINS
from core.db import init_db
from services.model_registry import ensure_default_model_registered

app = FastAPI(title="Traffic Sign Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dataset.router)
app.include_router(training.router)
app.include_router(models.router)
app.include_router(predict.router)
app.include_router(tools.router)


@app.on_event("startup")
def startup() -> None:
    init_db()
    ensure_default_model_registered()
    state.reload_active_predictor()
    state.refresh_dataset_cache()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": state.predictor is not None,
        "active_model": state.active_model_cache["version"] if state.active_model_cache else None,
    }
