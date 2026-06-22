from __future__ import annotations

import json
import time
from io import BytesIO
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from PIL import Image
from pydantic import BaseModel

from core.config import CLASS_LABEL_TO_ID, CLASS_NAMES, DATA_DIR
from tools.annotate import build_annotate_html
from tools.tambahan import (
    TAMBAHAN_DIR,
    build_tambahan_html,
    get_images_page,
    list_image_sources,
    move_images,
)
from tools.video_demo import build_video_demo_html

router = APIRouter(tags=["tools"])


class MoveRequest(BaseModel):
    paths: list[str]
    class_label: str
    split: str


@router.get("/video-demo", response_class=HTMLResponse)
def video_demo():
    return HTMLResponse(build_video_demo_html())


@router.get("/impor", response_class=HTMLResponse)
def tambahan_page():
    return HTMLResponse(content=build_tambahan_html(CLASS_NAMES))


@router.get("/tambahan/api/sources")
def tambahan_sources():
    return list_image_sources()


@router.get("/tambahan/api/images")
def tambahan_images(source: str = "", page: int = 1, per_page: int = 20):
    per_page = max(1, min(per_page, 200))
    return get_images_page(source, page, per_page)


@router.get("/tambahan/img/{path:path}")
def tambahan_image(path: str):
    img_path = (TAMBAHAN_DIR / path).resolve()
    try:
        img_path.relative_to(TAMBAHAN_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=400, detail="Path tidak valid")
    if not img_path.exists():
        raise HTTPException(status_code=404, detail="Gambar tidak ditemukan")
    return FileResponse(img_path)


@router.post("/tambahan/move")
def tambahan_move(req: MoveRequest):
    if req.class_label not in CLASS_LABEL_TO_ID:
        raise HTTPException(status_code=400, detail=f"Kelas tidak dikenal: {req.class_label}")
    if req.split not in ("train", "test"):
        raise HTTPException(status_code=400, detail="Split harus 'train' atau 'test'")
    if not req.paths:
        raise HTTPException(status_code=400, detail="Tidak ada gambar yang dipilih")
    result = move_images(req.paths, req.class_label, req.split, CLASS_LABEL_TO_ID, DATA_DIR)
    return result


@router.get("/annotate", response_class=HTMLResponse)
def annotate_page():
    return HTMLResponse(content=build_annotate_html(CLASS_NAMES))


@router.post("/data/save-annotation")
async def save_annotation(
    file: UploadFile = File(...),
    annotations: str = Form(...),
    class_label: str = Form(...),
    split: str = Form(...),
    img_width: int = Form(...),
    img_height: int = Form(...),
):
    if class_label not in CLASS_LABEL_TO_ID:
        raise HTTPException(status_code=400, detail=f"Kelas tidak dikenal: {class_label}")

    if split not in ("train", "test"):
        raise HTTPException(status_code=400, detail="Split harus 'train' atau 'test'")

    try:
        ann_list: list[dict] = json.loads(annotations)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Format annotations tidak valid") from exc

    if not ann_list:
        raise HTTPException(status_code=400, detail="Minimal satu anotasi bbox diperlukan")

    contents = await file.read()
    try:
        image = Image.open(BytesIO(contents)).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail="File gambar tidak valid") from exc

    iw, ih = image.size

    dest_dir = DATA_DIR / split / class_label
    dest_dir.mkdir(parents=True, exist_ok=True)

    original_stem = Path(file.filename or "image").stem
    suffix = Path(file.filename or "image.jpg").suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".bmp"}:
        suffix = ".jpg"
    ts = int(time.time() * 1000) % 1_000_000
    dest_img = dest_dir / f"{original_stem}_{ts}{suffix}"
    while dest_img.exists():
        ts += 1
        dest_img = dest_dir / f"{original_stem}_{ts}{suffix}"

    image.save(dest_img)

    class_id = CLASS_LABEL_TO_ID[class_label]
    lines: list[str] = []
    for ann in ann_list:
        try:
            x1 = max(0, min(int(ann["x1"]), iw))
            y1 = max(0, min(int(ann["y1"]), ih))
            x2 = max(0, min(int(ann["x2"]), iw))
            y2 = max(0, min(int(ann["y2"]), ih))
        except (KeyError, TypeError, ValueError) as exc:
            dest_img.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail=f"Format bbox tidak valid: {exc}") from exc

        cx = (x1 + x2) / 2.0 / iw
        cy = (y1 + y2) / 2.0 / ih
        w = abs(x2 - x1) / iw
        h = abs(y2 - y1) / ih
        lines.append(f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

    dest_txt = dest_img.with_suffix(".txt")
    dest_txt.write_text("\n".join(lines), encoding="utf-8")

    rel = str(dest_img.relative_to(DATA_DIR.parent.parent))
    return {
        "saved_as": rel,
        "class_label": class_label,
        "split": split,
        "bbox_count": len(lines),
        "image_size": [iw, ih],
    }
