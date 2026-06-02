from __future__ import annotations

from datetime import datetime

import torch
from torch.utils.data import DataLoader
from transformers import YolosImageProcessor

from app.schemas import TrainingRequest
from config import DATA_DIR, MODELS_ROOT
from dataset import TrafficSignDataset, collate_fn
from db import create_training_run, update_training_run, upsert_model, utc_now
from evaluation import evaluate_model
from training_core import build_model, train_one_epoch


def _build_scheduler(
    optimizer,
    total_epochs: int,
    warmup_epochs: int,
    cosine_decay: bool,
    lr_step: int,
    lr_gamma: float,
):
    if warmup_epochs > 0 and cosine_decay:
        # Linear warmup kemudian cosine annealing
        def warmup_lr_lambda(epoch: int) -> float:
            if epoch < warmup_epochs:
                return float(epoch + 1) / float(warmup_epochs)
            return 1.0

        warmup_scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=warmup_lr_lambda)
        cosine_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=max(total_epochs - warmup_epochs, 1),
            eta_min=1e-6,
        )
        return torch.optim.lr_scheduler.SequentialLR(
            optimizer,
            schedulers=[warmup_scheduler, cosine_scheduler],
            milestones=[warmup_epochs],
        )

    if lr_step > 0:
        return torch.optim.lr_scheduler.StepLR(
            optimizer,
            step_size=lr_step,
            gamma=lr_gamma,
        )

    return None


def build_output_version(request: TrainingRequest) -> str:
    if request.output_version:
        return request.output_version
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    return f"model-{timestamp}"


def materialize_training_request(request: TrainingRequest) -> TrainingRequest:
    return request.model_copy(update={"output_version": build_output_version(request)})


def get_selected_classes(request: TrainingRequest) -> list[str]:
    return list(request.selected_classes)


def create_training_run_record(request: TrainingRequest) -> dict:
    output_version = build_output_version(request)
    output_dir = str(MODELS_ROOT / output_version)
    return create_training_run(
        run_name=request.run_name,
        selected_classes=get_selected_classes(request),
        request=request.model_dump(),
        output_dir=output_dir,
        status="queued",
    )


def execute_training_run(run_id: int, request: TrainingRequest) -> dict | None:
    selected_classes = get_selected_classes(request)
    output_version = build_output_version(request)
    output_dir = MODELS_ROOT / output_version
    output_dir.mkdir(parents=True, exist_ok=True)

    update_training_run(run_id, status="running")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cuda":
        torch.backends.cudnn.benchmark = True

    try:
        train_dataset = TrafficSignDataset(DATA_DIR, "train", selected_classes)
        test_dataset = TrafficSignDataset(DATA_DIR, "test", selected_classes)
        train_loader = DataLoader(
            train_dataset,
            batch_size=request.batch_size,
            shuffle=True,
            num_workers=request.num_workers,
            collate_fn=collate_fn,
        )

        processor = YolosImageProcessor.from_pretrained(request.model_name)
        processor.size = {
            "shortest_edge": request.image_size,
            "longest_edge": request.image_size,
        }
        model = build_model(request.model_name, selected_classes)
        model.to(device)

        optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=request.learning_rate,
            weight_decay=request.weight_decay,
        )

        scheduler = _build_scheduler(
            optimizer=optimizer,
            total_epochs=request.epochs,
            warmup_epochs=request.warmup_epochs,
            cosine_decay=request.cosine_decay,
            lr_step=request.lr_step,
            lr_gamma=request.lr_gamma,
        )

        use_amp = request.use_amp and device.type == "cuda"
        scaler = torch.cuda.amp.GradScaler(enabled=use_amp)
        loss_history: list[dict[str, float]] = []

        for epoch in range(1, request.epochs + 1):
            avg_loss = train_one_epoch(
                model,
                processor,
                optimizer,
                train_loader,
                device,
                scaler,
                use_amp,
                grad_clip=request.grad_clip,
            )
            if scheduler is not None:
                scheduler.step()
            loss_history.append({"epoch": epoch, "loss": float(avg_loss)})

        model.save_pretrained(output_dir)
        processor.save_pretrained(output_dir)

        metrics = evaluate_model(
            model=model,
            processor=processor,
            dataset=test_dataset,
            class_names=selected_classes,
            device=device,
            score_threshold=request.score_threshold,
            iou_threshold=0.5,
        )
        metrics["loss_history"] = loss_history

        model_record = upsert_model(
            version=output_version,
            display_name=request.run_name,
            model_name=request.model_name,
            path=str(output_dir),
            status="ready",
            class_names=selected_classes,
            metrics=metrics,
            config=request.model_dump(),
            is_active=request.activate_after_training,
        )
        update_training_run(
            run_id,
            status="completed",
            model_id=model_record["id"],
            metrics=metrics,
            completed_at=utc_now(),
        )
        return model_record
    except Exception as exc:
        update_training_run(
            run_id,
            status="failed",
            error_message=str(exc),
            completed_at=utc_now(),
        )
        raise
