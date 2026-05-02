import argparse
from pathlib import Path
import time

import torch
from torch.utils.data import DataLoader
from transformers import YolosImageProcessor

from config import CLASS_NAMES, DATA_DIR, MODEL_DIR
from dataset import TrafficSignDataset, collate_fn
from training_core import build_model, train_one_epoch


def main():
    parser = argparse.ArgumentParser(description="Train YOLOS (Vision Transformer)")
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--lr-step", type=int, default=0)
    parser.add_argument("--lr-gamma", type=float, default=0.5)
    parser.add_argument("--num-workers", type=int, default=2)
    parser.add_argument("--model-name", type=str, default="hustvl/yolos-tiny")
    parser.add_argument("--image-size", type=int, default=512)
    parser.add_argument("--output-dir", type=Path, default=MODEL_DIR)
    parser.add_argument("--amp", action="store_true")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cuda":
        torch.backends.cudnn.benchmark = True

    train_dataset = TrafficSignDataset(args.data_dir, "train", CLASS_NAMES)
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        collate_fn=collate_fn,
    )

    processor = YolosImageProcessor.from_pretrained(args.model_name)
    processor.size = {"shortest_edge": args.image_size, "longest_edge": args.image_size}
    model = build_model(args.model_name, CLASS_NAMES)
    model.to(device)

    optimizer = torch.optim.AdamW(
        model.parameters(), lr=args.lr, weight_decay=args.weight_decay
    )
    scheduler = None
    if args.lr_step > 0:
        scheduler = torch.optim.lr_scheduler.StepLR(
            optimizer, step_size=args.lr_step, gamma=args.lr_gamma
        )
    use_amp = args.amp and device.type == "cuda"
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)

    start_time = time.time()
    for epoch in range(1, args.epochs + 1):
        avg_loss = train_one_epoch(
            model, processor, optimizer, train_loader, device, scaler, use_amp
        )
        if scheduler is not None:
            scheduler.step()
        elapsed = time.time() - start_time
        print(f"epoch={epoch} loss={avg_loss:.4f} elapsed={elapsed:.1f}s")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(args.output_dir)
    processor.save_pretrained(args.output_dir)
    print(f"saved model to {args.output_dir}")


if __name__ == "__main__":
    main()
