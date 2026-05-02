from __future__ import annotations

from pathlib import Path

from config import CLASS_NAMES, MODEL_NAME, MODEL_PATH
from db import get_active_model, get_model, init_db, set_active_model, upsert_model


def ensure_default_model_registered() -> dict | None:
    init_db()
    active_model = get_active_model()
    if active_model is not None:
        return active_model

    if not MODEL_PATH.exists():
        return None

    default_model = upsert_model(
        version=MODEL_PATH.name,
        display_name=MODEL_PATH.name,
        model_name=MODEL_NAME,
        path=str(MODEL_PATH),
        status="ready",
        class_names=list(CLASS_NAMES),
        metrics=None,
        config={"source": "filesystem-default"},
        is_active=True,
    )
    return default_model


def activate_model(model_id: int) -> dict | None:
    return set_active_model(model_id)


def resolve_active_model_path() -> tuple[dict | None, Path | None]:
    active_model = get_active_model()
    if active_model is None:
        return None, None

    model_path = Path(active_model["path"])
    if not model_path.exists():
        return active_model, None
    return active_model, model_path


def get_model_or_none(model_id: int) -> dict | None:
    return get_model(model_id)
