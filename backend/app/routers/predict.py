from __future__ import annotations

from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image

import app.state as state
from app.schemas import PredictionResponse
from core.config import SCORE_THRESHOLD

router = APIRouter(tags=["predict"])


@router.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...), score_threshold: float = SCORE_THRESHOLD):
    if state.predictor is None or state.active_model_cache is None:
        raise HTTPException(status_code=503, detail="No active model is loaded")
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()
    try:
        image = Image.open(BytesIO(contents)).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid image file") from exc

    results = state.predictor.predict(image, score_threshold=score_threshold)
    return PredictionResponse(
        model_id=state.active_model_cache["id"],
        model_version=state.active_model_cache["version"],
        model_display_name=state.active_model_cache["display_name"],
        score_threshold=score_threshold,
        image_width=image.width,
        image_height=image.height,
        detections=results,
    )
