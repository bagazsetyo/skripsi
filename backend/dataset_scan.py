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


@dataclass(frozen=True)
class ValidationIssue:
    split: str
    directory: str
    file: str
    issue_type: str
    detail: str


def _count_annotations(label_path: Path) -> int:
    count = 0
    for line in label_path.read_text().splitlines():
        if line.strip():
            count += 1
    return count


def _validate_yolo_line(
    line: str, split_name: str, class_dir: Path, label_path: Path
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    stripped = line.strip()
    if not stripped:
        return issues

    parts = stripped.split()
    if len(parts) != 5:
        issues.append(
            ValidationIssue(
                split=split_name,
                directory=class_dir.name,
                file=label_path.name,
                issue_type="invalid_annotation_format",
                detail=f"Expected 5 values, found {len(parts)}",
            )
        )
        return issues

    try:
        class_id = int(float(parts[0]))
        x_center, y_center, box_w, box_h = [float(value) for value in parts[1:]]
    except ValueError:
        issues.append(
            ValidationIssue(
                split=split_name,
                directory=class_dir.name,
                file=label_path.name,
                issue_type="invalid_annotation_format",
                detail="Annotation contains non-numeric values",
            )
        )
        return issues

    if class_id not in {item.class_id for item in TRAFFIC_SIGN_CLASSES}:
        issues.append(
            ValidationIssue(
                split=split_name,
                directory=class_dir.name,
                file=label_path.name,
                issue_type="invalid_class_id",
                detail=f"class_id {class_id} is not registered",
            )
        )

    bbox_values = {
        "x_center": x_center,
        "y_center": y_center,
        "width": box_w,
        "height": box_h,
    }
    invalid_bbox_fields = [
        name
        for name, value in bbox_values.items()
        if value < 0 or value > 1
    ]
    if invalid_bbox_fields:
        issues.append(
            ValidationIssue(
                split=split_name,
                directory=class_dir.name,
                file=label_path.name,
                issue_type="invalid_bbox",
                detail=f"Out-of-range YOLO values in: {', '.join(invalid_bbox_fields)}",
            )
        )

    if box_w <= 0 or box_h <= 0:
        issues.append(
            ValidationIssue(
                split=split_name,
                directory=class_dir.name,
                file=label_path.name,
                issue_type="invalid_bbox",
                detail="Bounding box width and height must be greater than zero",
            )
        )

    return issues


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


def validate_split(split_dir: Path) -> dict:
    issues: list[ValidationIssue] = []

    for traffic_sign_class in TRAFFIC_SIGN_CLASSES:
        class_dir = split_dir / traffic_sign_class.directory
        if not class_dir.exists():
            continue

        image_files = {
            path.stem: path.name
            for path in class_dir.iterdir()
            if path.suffix.lower() in IMAGE_EXTS
        }
        label_files = {
            path.stem: path
            for path in class_dir.iterdir()
            if path.suffix.lower() == ".txt"
        }

        for image_stem, image_name in image_files.items():
            if image_stem not in label_files:
                issues.append(
                    ValidationIssue(
                        split=split_dir.name,
                        directory=class_dir.name,
                        file=image_name,
                        issue_type="missing_label_file",
                        detail="Image file does not have matching .txt label",
                    )
                )

        for label_stem, label_path in label_files.items():
            if label_stem not in image_files:
                issues.append(
                    ValidationIssue(
                        split=split_dir.name,
                        directory=class_dir.name,
                        file=label_path.name,
                        issue_type="missing_image_file",
                        detail="Label file does not have matching image",
                    )
                )

            lines = label_path.read_text().splitlines()
            non_empty_lines = [line for line in lines if line.strip()]
            if not non_empty_lines:
                issues.append(
                    ValidationIssue(
                        split=split_dir.name,
                        directory=class_dir.name,
                        file=label_path.name,
                        issue_type="empty_label_file",
                        detail="Label file exists but has no annotation lines",
                    )
                )
                continue

            for line in non_empty_lines:
                issues.extend(
                    _validate_yolo_line(line, split_dir.name, class_dir, label_path)
                )

    issue_dicts = [asdict(issue) for issue in issues]
    issue_counts: dict[str, int] = {}
    for issue in issues:
        issue_counts[issue.issue_type] = issue_counts.get(issue.issue_type, 0) + 1

    return {
        "split": split_dir.name,
        "is_valid": len(issues) == 0,
        "issue_count": len(issues),
        "issue_counts": issue_counts,
        "issues": issue_dicts,
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


def validate_dataset(root_dir: Path = DATA_DIR) -> dict:
    train_validation = validate_split(root_dir / "train")
    test_validation = validate_split(root_dir / "test")
    total_issue_count = train_validation["issue_count"] + test_validation["issue_count"]

    aggregated_issue_counts: dict[str, int] = {}
    for validation in (train_validation, test_validation):
        for issue_type, count in validation["issue_counts"].items():
            aggregated_issue_counts[issue_type] = (
                aggregated_issue_counts.get(issue_type, 0) + count
            )

    return {
        "root_dir": str(root_dir),
        "is_valid": total_issue_count == 0,
        "issue_count": total_issue_count,
        "issue_counts": aggregated_issue_counts,
        "splits": {
            "train": train_validation,
            "test": test_validation,
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
        "validation": validate_dataset(DATA_DIR),
        "paths": {
            "train_dir": str(TRAIN_DIR),
            "test_dir": str(TEST_DIR),
        },
        "class_lookup": build_class_lookup(),
    }
    print(json.dumps(summary, indent=2))
