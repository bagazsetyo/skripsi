from io import BytesIO

from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image
import torch

from config import CLASS_NAMES, MODEL_PATH, SCORE_THRESHOLD
from app.inference import Predictor

app = FastAPI(title="Traffic Sign Detection API")

predictor: Predictor | None = None


@app.on_event("startup")
def load_model():
    global predictor
    if not MODEL_PATH.exists():
        raise RuntimeError(
            f"Model not found at {MODEL_PATH}. Train the model before starting the API."
        )
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    predictor = Predictor(MODEL_PATH, CLASS_NAMES, device)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...), score_threshold: float = SCORE_THRESHOLD):
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()
    try:
        image = Image.open(BytesIO(contents)).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid image file") from exc

    results = predictor.predict(image, score_threshold=score_threshold)
    return results
