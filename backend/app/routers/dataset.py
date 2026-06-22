from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse

import app.state as state
from app.auth import get_current_admin
from core.config import DATA_DIR
from services.dataset import IMAGE_EXTS
from services.dataset_scan import build_class_lookup

router = APIRouter(prefix="/dataset", tags=["dataset"])


@router.get("/classes")
def dataset_classes(_: dict = Depends(get_current_admin)):
    return build_class_lookup()


@router.get("/summary")
def dataset_summary(_: dict = Depends(get_current_admin)):
    return state.get_dataset_cache_payload("summary")


@router.get("/validation")
def dataset_validation(_: dict = Depends(get_current_admin)):
    return state.get_dataset_cache_payload("validation")


@router.post("/refresh")
def dataset_refresh(background_tasks: BackgroundTasks, _: dict = Depends(get_current_admin)):
    if state.dataset_refresh_state["is_refreshing"]:
        return {
            "status": "running",
            "message": "Dataset refresh is already running in the background.",
            "last_started_at": state.dataset_refresh_state["last_started_at"],
        }
    background_tasks.add_task(state.run_dataset_refresh_job)
    return {
        "status": "queued",
        "message": "Dataset refresh has started in the background.",
    }


@router.get("/images")
def dataset_images(
    split: str,
    class_label: str,
    page: int = 1,
    per_page: int = 30,
    _: dict = Depends(get_current_admin),
):
    if split not in ("train", "test"):
        raise HTTPException(status_code=400, detail="Split harus 'train' atau 'test'")

    class_dir = DATA_DIR / split / class_label
    if not class_dir.exists():
        return {"images": [], "total": 0, "page": 1, "per_page": per_page, "total_pages": 1}

    all_images = sorted(
        f.name for f in class_dir.iterdir() if f.suffix.lower() in IMAGE_EXTS
    )
    total = len(all_images)
    per_page = max(1, min(per_page, 100))
    total_pages = max(1, (total + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    chunk = all_images[(page - 1) * per_page : page * per_page]

    return {
        "images": [
            {"filename": name, "url": f"/dataset/img/{split}/{class_label}/{name}"}
            for name in chunk
        ],
        "split": split,
        "class_label": class_label,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
    }


@router.get("/img/{split}/{class_label}/{filename}")
def dataset_image(split: str, class_label: str, filename: str):
    if split not in ("train", "test"):
        raise HTTPException(status_code=400, detail="Split tidak valid")

    img_path = (DATA_DIR / split / class_label / filename).resolve()
    try:
        img_path.relative_to(DATA_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=400, detail="Path tidak valid")

    if not img_path.exists() or img_path.suffix.lower() not in IMAGE_EXTS:
        raise HTTPException(status_code=404, detail="Gambar tidak ditemukan")

    return FileResponse(img_path)
