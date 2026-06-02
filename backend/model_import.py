from __future__ import annotations

import json
import re
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

from config import MODELS_ROOT
from db import upsert_model


REQUIRED_MODEL_FILES = ("config.json", "preprocessor_config.json")
WEIGHT_FILES = ("pytorch_model.bin", "model.safetensors")


def _slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    normalized = normalized.strip("-._")
    return normalized or f"imported-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"


def _safe_extract_zip(archive_path: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive_path, "r") as archive:
        for member in archive.infolist():
            member_path = destination / member.filename
            resolved_destination = member_path.resolve()
            if destination.resolve() not in resolved_destination.parents and resolved_destination != destination.resolve():
                raise ValueError("ZIP archive contains an unsafe path")
        archive.extractall(destination)


def _is_model_directory(path: Path) -> bool:
    if not path.is_dir():
        return False
    has_required = all((path / filename).exists() for filename in REQUIRED_MODEL_FILES)
    has_weights = any((path / filename).exists() for filename in WEIGHT_FILES)
    return has_required and has_weights


def _find_model_directory(search_root: Path) -> Path:
    if _is_model_directory(search_root):
        return search_root

    direct_candidates = [path for path in search_root.iterdir() if _is_model_directory(path)]
    if len(direct_candidates) == 1:
        return direct_candidates[0]
    if len(direct_candidates) > 1:
        raise ValueError("ZIP contains multiple model directories. Please upload a single model archive.")

    recursive_candidates = [path for path in search_root.rglob("*") if _is_model_directory(path)]
    if len(recursive_candidates) == 1:
        return recursive_candidates[0]
    if len(recursive_candidates) > 1:
        raise ValueError("ZIP contains multiple model directories. Please upload a single model archive.")

    raise ValueError("No valid Hugging Face model directory found in ZIP archive.")


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _extract_class_names(config_data: dict[str, Any], training_summary: dict[str, Any] | None) -> list[str]:
    id2label = config_data.get("id2label")
    if isinstance(id2label, dict) and id2label:
        names: list[str] = []
        for key in sorted(id2label.keys(), key=lambda item: int(item) if str(item).isdigit() else str(item)):
            value = id2label[key]
            if isinstance(value, str):
                names.append(value)
        if names:
            return names

    if training_summary:
        preset_classes = training_summary.get("class_names")
        if isinstance(preset_classes, list) and all(isinstance(item, str) for item in preset_classes):
            return preset_classes

        metrics = training_summary.get("metrics")
        if isinstance(metrics, dict):
            per_class = metrics.get("per_class", [])
            class_names = [
                item.get("class_name")
                for item in per_class
                if isinstance(item, dict) and isinstance(item.get("class_name"), str)
            ]
            if class_names:
                return class_names

    raise ValueError("Unable to determine class names from the imported model.")


def _extract_metrics(training_summary: dict[str, Any] | None, metrics_data: dict[str, Any] | None) -> dict[str, Any] | None:
    if metrics_data:
        return metrics_data
    if training_summary and isinstance(training_summary.get("metrics"), dict):
        return training_summary["metrics"]
    return None


def import_model_archive(
    archive_path: Path,
    *,
    display_name: str | None = None,
    version: str | None = None,
    activate: bool = False,
) -> dict[str, Any]:
    if archive_path.suffix.lower() != ".zip":
        raise ValueError("Imported model must be a .zip archive.")

    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        _safe_extract_zip(archive_path, temp_dir)
        model_dir = _find_model_directory(temp_dir)

        config_data = _load_json(model_dir / "config.json") or {}
        training_summary = _load_json(model_dir / "training_summary.json")
        metrics_data = _load_json(model_dir / "metrics.json")
        preset_config = _load_json(model_dir / "preset_config.json")

        class_names = _extract_class_names(config_data, training_summary)
        metrics = _extract_metrics(training_summary, metrics_data)
        model_name = config_data.get("_name_or_path") or config_data.get("model_type") or "imported-model"

        resolved_version = _slugify(version or model_dir.name)
        target_dir = MODELS_ROOT / resolved_version
        if target_dir.exists():
            raise ValueError(f"Target model directory already exists: {target_dir.name}")

        shutil.copytree(model_dir, target_dir)

    record = upsert_model(
        version=resolved_version,
        display_name=display_name or resolved_version,
        model_name=str(model_name),
        path=str(target_dir),
        status="ready",
        class_names=class_names,
        metrics=metrics,
        config={
            "source": "zip-import",
            "imported_at": datetime.utcnow().isoformat() + "Z",
            "original_model_dir": model_dir.name,
            "preset_config": preset_config,
            "training_summary_present": training_summary is not None,
            "metrics_present": metrics is not None,
        },
        is_active=activate,
    )
    return record
