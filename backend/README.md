# Traffic Sign Detection Backend

This backend provides:
- Training script for Vision Transformer (YOLOS)
- FastAPI inference endpoint `/predict`
- Dataset summary and validation endpoints
- SQLite-based model registry and training run history

## Classes
Active classes are defined in `backend/config.py` under `CLASS_NAMES`.
Current repo configuration uses the full 21 traffic sign classes from the dataset.

## Train (GPU)
Build the Docker image from repo root:

```
docker build -t traffic-sign-backend -f backend/Dockerfile .
```

Run training with GPU and mount data + models:

```
docker run --rm --gpus all -v $(pwd)/data:/app/data -v $(pwd)/backend/models:/app/backend/models traffic-sign-backend python train.py --data-dir /app/data/traffic_sign --epochs 30 --batch-size 1 --image-size 512 --amp --lr-step 10 --lr-gamma 0.5 --model-name hustvl/yolos-tiny
```

The model will be saved to `backend/models/yolos`.

Note: the first training run downloads pretrained YOLOS weights from Hugging Face.

Tips:
- Increase `--epochs` to 30-50 for better confidence on small datasets.
- If you hit GPU OOM, keep `--batch-size` at 1 and lower `--image-size` (e.g. 448).
- Use `--amp` to reduce GPU memory usage on RTX 3050.
- You can swap model to `hustvl/yolos-tiny` or other YOLOS variants.

## API
Run the API with GPU (or CPU if no GPU available):

```
docker run --rm --gpus all -p 8000:8000 \
  -v $(pwd)/backend/models:/app/backend/models \
  traffic-sign-backend
```

You can adjust the score threshold with `SCORE_THRESHOLD` (default 0.5).
Data and model paths can also be overridden with `DATA_ROOT` and `MODELS_ROOT`.

## Docker Compose Development Mode

When running with `docker compose up backend`:
- local folder `backend/` is mounted into `/app/backend`
- API runs with `uvicorn --reload`
- Python source changes do not require image rebuild

You still need to rebuild if:
- `backend/requirements.txt` changes
- `backend/Dockerfile` changes
- container dependencies need to be refreshed

### Main endpoints

- `GET /health`
- `GET /dataset/classes`
- `GET /dataset/summary`
- `GET /dataset/validation`
- `GET /training/config`
- `POST /training/runs`
- `GET /training/runs`
- `GET /training/runs/{id}`
- `GET /models`
- `GET /models/active`
- `POST /models/{id}/activate`
- `GET /models/{id}/evaluation`
- `POST /predict`

### Predict
Example request:

```
curl -X POST "http://localhost:8000/predict" -F "file=@/path/to/image.jpg"
```

Response format:

```
[
  {
    "class": "larangan-berhenti",
    "confidence": 0.95,
    "box": [x_min, y_min, x_max, y_max]
  }
]
```
