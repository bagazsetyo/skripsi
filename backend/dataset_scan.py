from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from config import (
        CLASS_DIRECTORY_TO_ID,
        CLASS_DIRECTORY_TO_LABEL,
        DATA_DIR,
        TEST_DIR,
        TRAFFIC_SIGN_CLASSES,
        TRAIN_DIR,
    )
    from dataset import IMAGE_EXTS
except ModuleNotFoundError:
    from backend.config import (
        CLASS_DIRECTORY_TO_ID,
        CLASS_DIRECTORY_TO_LABEL,
        DATA_DIR,
        TEST_DIR,
        TRAFFIC_SIGN_CLASSES,
        TRAIN_DIR,
    )
    from backend.dataset import IMAGE_EXTS


@dataclass(frozen=True)
class ClassSplitStats:
    class_id: int
    label: str
    directory: str
    image_count: int
    label_file_count: int
    annotation_count: int


def _count_annotations(label_path: Path) -> int:
    count = 0
    for line in label_path.read_text().splitlines():
        if line.strip():
            count += 1
    return count


def scan_split(split_dir: Path) -> dict:
    class_stats: list[ClassSplitStats] = []
    total_images = 0
    total_label_files = 0
    total_annotations = 0

    for traffic_sign_class in TRAFFIC_SIGN_CLASSES:
        class_dir = split_dir / traffic_sign_class.directory
        image_count = 0
        label_file_count = 0
        annotation_count = 0

        if class_dir.exists():
            for path in class_dir.iterdir():
                if path.suffix.lower() in IMAGE_EXTS:
                    image_count += 1
                    continue
                if path.suffix.lower() == ".txt":
                    label_file_count += 1
                    annotation_count += _count_annotations(path)

        total_images += image_count
        total_label_files += label_file_count
        total_annotations += annotation_count
        class_stats.append(
            ClassSplitStats(
                class_id=traffic_sign_class.class_id,
                label=traffic_sign_class.label,
                directory=traffic_sign_class.directory,
                image_count=image_count,
                label_file_count=label_file_count,
                annotation_count=annotation_count,
            )
        )

    return {
        "split": split_dir.name,
        "class_count": len(class_stats),
        "image_count": total_images,
        "label_file_count": total_label_files,
        "annotation_count": total_annotations,
        "classes": [asdict(item) for item in class_stats],
    }


def scan_dataset(root_dir: Path = DATA_DIR) -> dict:
    train_summary = scan_split(root_dir / "train")
    test_summary = scan_split(root_dir / "test")

    return {
        "root_dir": str(root_dir),
        "expected_class_count": len(TRAFFIC_SIGN_CLASSES),
        "class_catalog": [
            {
                "class_id": traffic_sign_class.class_id,
                "label": traffic_sign_class.label,
                "directory": traffic_sign_class.directory,
            }
            for traffic_sign_class in TRAFFIC_SIGN_CLASSES
        ],
        "splits": {
            "train": train_summary,
            "test": test_summary,
        },
        "totals": {
            "class_count": len(TRAFFIC_SIGN_CLASSES),
            "image_count": train_summary["image_count"] + test_summary["image_count"],
            "label_file_count": train_summary["label_file_count"]
            + test_summary["label_file_count"],
            "annotation_count": train_summary["annotation_count"]
            + test_summary["annotation_count"],
        },
    }


def build_class_lookup() -> list[dict]:
    return [
        {
            "class_id": traffic_sign_class.class_id,
            "label": traffic_sign_class.label,
            "directory": traffic_sign_class.directory,
            "mapped_class_id": CLASS_DIRECTORY_TO_ID[traffic_sign_class.directory],
            "mapped_label": CLASS_DIRECTORY_TO_LABEL[traffic_sign_class.directory],
        }
        for traffic_sign_class in TRAFFIC_SIGN_CLASSES
    ]


if __name__ == "__main__":
    import json

    summary = {
        "dataset": scan_dataset(DATA_DIR),
        "paths": {
            "train_dir": str(TRAIN_DIR),
            "test_dir": str(TEST_DIR),
        },
        "class_lookup": build_class_lookup(),
    }
    print(json.dumps(summary, indent=2))
