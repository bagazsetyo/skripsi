from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "backend"
LOCAL_DATA_ROOT = REPO_ROOT / "data"
LOCAL_DATASET_DIR = LOCAL_DATA_ROOT / "traffic_sign"

DEFAULT_MODEL_NAME = "hustvl/yolos-tiny"
DEFAULT_DATASET_SOURCE = "/content/drive/MyDrive/skripsi-data/traffic_sign.zip"
DEFAULT_DRIVE_OUTPUT_ROOT = "/content/drive/MyDrive/skripsi-models"
DEFAULT_DRIVE_MOUNT_POINT = "/content/drive"


@dataclass(frozen=True)
class ExperimentPreset:
    preset_key: str
    run_name: str
    output_name: str
    image_size: int
    epochs: int
    batch_size: int
    learning_rate: float
    weight_decay: float
    score_threshold: float
    lr_step: int
    lr_gamma: float
    num_workers: int
    use_amp: bool


PRESETS: dict[str, ExperimentPreset] = {
    "img500": ExperimentPreset(
        preset_key="img500",
        run_name="yolos-image-500",
        output_name="yolos-image-500",
        image_size=500,
        epochs=30,
        batch_size=1,
        learning_rate=0.00005,
        weight_decay=0.0001,
        score_threshold=0.5,
        lr_step=10,
        lr_gamma=0.5,
        num_workers=2,
        use_amp=True,
    ),
    "img600": ExperimentPreset(
        preset_key="img600",
        run_name="yolos-image-600",
        output_name="yolos-image-600",
        image_size=600,
        epochs=30,
        batch_size=1,
        learning_rate=0.00005,
        weight_decay=0.0001,
        score_threshold=0.5,
        lr_step=10,
        lr_gamma=0.5,
        num_workers=2,
        use_amp=True,
    ),
    "img700": ExperimentPreset(
        preset_key="img700",
        run_name="yolos-image-700",
        output_name="yolos-image-700",
        image_size=700,
        epochs=30,
        batch_size=1,
        learning_rate=0.00005,
        weight_decay=0.0001,
        score_threshold=0.5,
        lr_step=10,
        lr_gamma=0.5,
        num_workers=2,
        use_amp=True,
    ),
}


def build_parser(default_preset: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Runner otomatis eksperimen YOLOS di Google Colab."
    )
    parser.add_argument(
        "--preset",
        default=default_preset,
        choices=sorted(PRESETS.keys()),
        help="Preset eksperimen yang akan dijalankan.",
    )
    parser.add_argument(
        "--dataset-source",
        default=DEFAULT_DATASET_SOURCE,
        help="Path dataset di Google Drive. Bisa folder atau file zip.",
    )
    parser.add_argument(
        "--drive-output-root",
        default=DEFAULT_DRIVE_OUTPUT_ROOT,
        help="Folder output model di Google Drive.",
    )
    parser.add_argument(
        "--model-name",
        default=DEFAULT_MODEL_NAME,
        help="Nama model Hugging Face YOLOS.",
    )
    parser.add_argument(
        "--drive-mount-point",
        default=DEFAULT_DRIVE_MOUNT_POINT,
        help="Lokasi mount Google Drive.",
    )
    parser.add_argument(
        "--output-name",
        default="",
        help="Nama folder output model. Jika kosong, memakai nama preset.",
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Lewati install dependency bila environment sudah siap.",
    )
    parser.add_argument(
        "--skip-mount",
        action="store_true",
        help="Lewati mount Google Drive bila sudah ter-mount.",
    )
    parser.add_argument(
        "--force-dataset-copy",
        action="store_true",
        help="Paksa copy/unzip ulang dataset ke folder lokal repo.",
    )
    return parser


def is_running_in_colab() -> bool:
    try:
        import google.colab  # type: ignore  # noqa: F401
    except ImportError:
        return False
    return True


def ensure_google_drive_mounted(mount_point: Path) -> None:
    if (mount_point / "MyDrive").exists():
        print(f"[INFO] Google Drive sudah ter-mount di {mount_point}.")
        return

    if not is_running_in_colab():
        raise RuntimeError(
            "Google Drive belum ter-mount dan script tidak berjalan di Google Colab."
        )

    from google.colab import drive  # type: ignore

    print(f"[INFO] Mount Google Drive ke {mount_point} ...")
    drive.mount(str(mount_point))


def install_requirements() -> None:
    requirements_path = BACKEND_ROOT / "requirements.txt"
    print(f"[INFO] Install dependency dari {requirements_path} ...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)],
        check=True,
    )


def locate_dataset_dir(base_dir: Path) -> Path | None:
    if (base_dir / "train").exists() and (base_dir / "test").exists():
        return base_dir

    for child in base_dir.iterdir():
        if child.is_dir() and (child / "train").exists() and (child / "test").exists():
            return child

    return None


def prepare_dataset(dataset_source: Path, *, force_copy: bool) -> Path:
    if LOCAL_DATASET_DIR.exists() and not force_copy:
        print(f"[INFO] Dataset lokal sudah ada di {LOCAL_DATASET_DIR}, skip copy.")
        return LOCAL_DATASET_DIR

    if LOCAL_DATASET_DIR.exists():
        shutil.rmtree(LOCAL_DATASET_DIR)

    LOCAL_DATA_ROOT.mkdir(parents=True, exist_ok=True)

    if not dataset_source.exists():
        raise FileNotFoundError(f"Dataset source tidak ditemukan: {dataset_source}")

    print(f"[INFO] Menyiapkan dataset dari {dataset_source} ...")

    if dataset_source.is_dir():
        dataset_dir = locate_dataset_dir(dataset_source)
        if dataset_dir is None:
            raise ValueError(
                "Folder dataset source tidak berisi struktur train/test yang valid."
            )
        shutil.copytree(dataset_dir, LOCAL_DATASET_DIR)
        return LOCAL_DATASET_DIR

    if dataset_source.suffix.lower() == ".zip":
        with tempfile.TemporaryDirectory() as temp_dir_str:
            temp_dir = Path(temp_dir_str)
            with zipfile.ZipFile(dataset_source, "r") as archive:
                archive.extractall(temp_dir)

            dataset_dir = locate_dataset_dir(temp_dir)
            if dataset_dir is None:
                raise ValueError(
                    "Isi zip dataset tidak mengandung struktur folder train/test yang valid."
                )
            shutil.copytree(dataset_dir, LOCAL_DATASET_DIR)
            return LOCAL_DATASET_DIR

    raise ValueError("Dataset source harus berupa folder atau file .zip")


def import_training_modules():
    if str(BACKEND_ROOT) not in sys.path:
        sys.path.insert(0, str(BACKEND_ROOT))

    import torch
    from torch.utils.data import DataLoader
    from transformers import YolosImageProcessor

    from config import CLASS_NAMES
    from dataset import TrafficSignDataset, collate_fn
    from evaluation import evaluate_model
    from training_core import build_model, train_one_epoch

    return {
        "torch": torch,
        "DataLoader": DataLoader,
        "YolosImageProcessor": YolosImageProcessor,
        "CLASS_NAMES": CLASS_NAMES,
        "TrafficSignDataset": TrafficSignDataset,
        "collate_fn": collate_fn,
        "evaluate_model": evaluate_model,
        "build_model": build_model,
        "train_one_epoch": train_one_epoch,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def run_experiment(
    preset: ExperimentPreset,
    *,
    dataset_dir: Path,
    output_dir: Path,
    model_name: str,
) -> dict[str, Any]:
    modules = import_training_modules()
    torch = modules["torch"]
    DataLoader = modules["DataLoader"]
    YolosImageProcessor = modules["YolosImageProcessor"]
    CLASS_NAMES = modules["CLASS_NAMES"]
    TrafficSignDataset = modules["TrafficSignDataset"]
    collate_fn = modules["collate_fn"]
    evaluate_model = modules["evaluate_model"]
    build_model = modules["build_model"]
    train_one_epoch = modules["train_one_epoch"]

    output_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cuda":
        torch.backends.cudnn.benchmark = True

    train_dataset = TrafficSignDataset(dataset_dir, "train", CLASS_NAMES)
    test_dataset = TrafficSignDataset(dataset_dir, "test", CLASS_NAMES)
    train_loader = DataLoader(
        train_dataset,
        batch_size=preset.batch_size,
        shuffle=True,
        num_workers=preset.num_workers,
        collate_fn=collate_fn,
    )

    processor = YolosImageProcessor.from_pretrained(model_name)
    processor.size = {
        "shortest_edge": preset.image_size,
        "longest_edge": preset.image_size,
    }
    model = build_model(model_name, CLASS_NAMES)
    model.to(device)

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=preset.learning_rate,
        weight_decay=preset.weight_decay,
    )
    scheduler = None
    if preset.lr_step > 0:
        scheduler = torch.optim.lr_scheduler.StepLR(
            optimizer,
            step_size=preset.lr_step,
            gamma=preset.lr_gamma,
        )

    use_amp = preset.use_amp and device.type == "cuda"
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)

    print("[INFO] Mulai training ...")
    started_at = time.time()
    loss_history: list[dict[str, float]] = []

    for epoch in range(1, preset.epochs + 1):
        avg_loss = train_one_epoch(
            model,
            processor,
            optimizer,
            train_loader,
            device,
            scaler,
            use_amp,
        )
        if scheduler is not None:
            scheduler.step()

        epoch_elapsed = time.time() - started_at
        loss_history.append({"epoch": epoch, "loss": float(avg_loss)})
        print(
            f"[TRAIN] preset={preset.preset_key} epoch={epoch}/{preset.epochs} "
            f"loss={avg_loss:.4f} elapsed={epoch_elapsed:.1f}s"
        )

    print("[INFO] Menyimpan model dan processor ...")
    model.save_pretrained(output_dir)
    processor.save_pretrained(output_dir)

    print("[INFO] Menjalankan evaluasi ...")
    metrics = evaluate_model(
        model=model,
        processor=processor,
        dataset=test_dataset,
        class_names=CLASS_NAMES,
        device=device,
        score_threshold=preset.score_threshold,
        iou_threshold=0.5,
    )
    metrics["loss_history"] = loss_history

    completed_at = time.time()
    summary = {
        "preset": asdict(preset),
        "model_name": model_name,
        "output_dir": str(output_dir),
        "dataset_dir": str(dataset_dir),
        "device": str(device),
        "train_samples": len(train_dataset),
        "test_samples": len(test_dataset),
        "started_at_unix": started_at,
        "completed_at_unix": completed_at,
        "training_seconds": completed_at - started_at,
        "metrics": metrics,
    }

    write_json(output_dir / "training_summary.json", summary)
    write_json(output_dir / "metrics.json", metrics)
    write_json(output_dir / "preset_config.json", asdict(preset))
    return summary


def main_for_preset(default_preset: str) -> None:
    parser = build_parser(default_preset)
    args = parser.parse_args()
    preset = PRESETS[args.preset]

    drive_mount_point = Path(args.drive_mount_point)
    if not args.skip_mount:
        ensure_google_drive_mounted(drive_mount_point)

    if not args.skip_install:
        install_requirements()

    dataset_source = Path(args.dataset_source)
    dataset_dir = prepare_dataset(dataset_source, force_copy=args.force_dataset_copy)

    output_name = args.output_name or preset.output_name
    output_dir = Path(args.drive_output_root) / output_name

    print(
        f"[INFO] Menjalankan preset {preset.preset_key} | "
        f"image_size={preset.image_size} | output={output_dir}"
    )
    summary = run_experiment(
        preset,
        dataset_dir=dataset_dir,
        output_dir=output_dir,
        model_name=args.model_name,
    )
    print("[DONE] Training dan evaluasi selesai.")
    print(json.dumps(summary["metrics"], indent=2, ensure_ascii=True))
    print(f"[DONE] Artifact tersimpan di: {output_dir}")

