from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}


def _read_yolo_ids(label_path: Path) -> List[int]:
    ids: List[int] = []
    for line in label_path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        ids.append(int(float(parts[0])))
    return ids


def infer_yolo_id_for_class(class_dir: Path) -> int:
    if not class_dir.exists():
        raise FileNotFoundError(f"Class directory not found: {class_dir}")
    yolo_ids = set()
    for label_path in class_dir.glob("*.txt"):
        ids = _read_yolo_ids(label_path)
        yolo_ids.update(ids)
    if not yolo_ids:
        raise ValueError(f"No YOLO labels found in {class_dir}")
    if len(yolo_ids) != 1:
        raise ValueError(
            f"Multiple class ids found in {class_dir}: {sorted(yolo_ids)}"
        )
    return next(iter(yolo_ids))


def build_class_maps(
    split_dir: Path, class_names: List[str]
) -> Tuple[Dict[str, int], Dict[int, int]]:
    class_to_yolo: Dict[str, int] = {}
    for name in class_names:
        class_dir = split_dir / name
        class_to_yolo[name] = infer_yolo_id_for_class(class_dir)
    yolo_to_label = {class_to_yolo[name]: idx for idx, name in enumerate(class_names)}
    return class_to_yolo, yolo_to_label


def collect_samples(split_dir: Path, class_names: List[str]) -> List[Tuple[Path, Path]]:
    items: List[Tuple[Path, Path]] = []
    for name in class_names:
        class_dir = split_dir / name
        if not class_dir.exists():
            continue
        for path in class_dir.iterdir():
            if path.suffix.lower() not in IMAGE_EXTS:
                continue
            label_path = path.with_suffix(".txt")
            if not label_path.exists():
                continue
            items.append((path, label_path))
    if not items:
        raise ValueError(f"No images found in {split_dir} for {class_names}")
    return items


def _yolo_to_xywh(values: List[float], width: int, height: int) -> List[float]:
    _, x_center, y_center, box_w, box_h = values
    x_min = (x_center - box_w / 2.0) * width
    y_min = (y_center - box_h / 2.0) * height
    return [x_min, y_min, box_w * width, box_h * height]


class TrafficSignDataset:
    def __init__(self, root_dir: Path, split: str, class_names: List[str]):
        self.split_dir = Path(root_dir) / split
        self.class_names = class_names
        self.class_to_yolo, self.yolo_to_label = build_class_maps(
            self.split_dir, class_names
        )
        self.items = collect_samples(self.split_dir, class_names)

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int):
        image_path, label_path = self.items[index]
        image = Image.open(image_path).convert("RGB")
        width, height = image.size

        annotations: List[Dict[str, float]] = []
        for line in label_path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            parts = [float(x) for x in line.split()]
            if len(parts) < 5:
                continue
            yolo_id = int(parts[0])
            if yolo_id not in self.yolo_to_label:
                continue
            bbox = _yolo_to_xywh(parts, width, height)
            area = bbox[2] * bbox[3]
            annotations.append(
                {
                    "bbox": bbox,
                    "category_id": self.yolo_to_label[yolo_id],
                    "area": area,
                    "iscrowd": 0,
                }
            )

        target = {"image_id": index, "annotations": annotations}
        return image, target


def collate_fn(batch):
    images, targets = zip(*batch)
    return list(images), list(targets)
