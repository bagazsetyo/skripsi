from __future__ import annotations

import torch
from transformers import YolosForObjectDetection


def build_model(model_name: str, class_names: list[str]):
    id2label = {idx: name for idx, name in enumerate(class_names)}
    label2id = {name: idx for idx, name in enumerate(class_names)}
    return YolosForObjectDetection.from_pretrained(
        model_name,
        num_labels=len(class_names),
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True,
    )


def train_one_epoch(model, processor, optimizer, loader, device, scaler=None, amp=False, grad_clip: float = 0.1):
    model.train()
    running_loss = 0.0
    for images, targets in loader:
        encoding = processor(images=images, annotations=targets, return_tensors="pt")
        pixel_values = encoding["pixel_values"].to(device)
        labels = [
            {k: v.to(device) for k, v in label.items()} for label in encoding["labels"]
        ]

        optimizer.zero_grad()
        with torch.cuda.amp.autocast(enabled=amp):
            outputs = model(pixel_values=pixel_values, labels=labels)
            loss = outputs.loss
        if amp and scaler is not None:
            scaler.scale(loss).backward()
            if grad_clip > 0:
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=grad_clip)
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            if grad_clip > 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=grad_clip)
            optimizer.step()

        running_loss += loss.item()

    return running_loss / max(len(loader), 1)
