from __future__ import annotations

from typing import List

from PIL import Image
import torch
from transformers import YolosForObjectDetection, YolosImageProcessor


def _load_class_names(model, fallback: List[str]) -> List[str]:
    id2label = getattr(model.config, "id2label", None)
    if not id2label:
        return fallback
    if all(isinstance(k, str) for k in id2label.keys()):
        return [id2label[str(i)] for i in range(len(id2label))]
    return [id2label[i] for i in range(len(id2label))]


class Predictor:
    def __init__(self, model_path, class_names: List[str], device: torch.device):
        self.device = device
        self.model = YolosForObjectDetection.from_pretrained(model_path)
        self.processor = YolosImageProcessor.from_pretrained(model_path)
        self.model.to(device).eval()
        self.class_names = _load_class_names(self.model, class_names)

    def predict(self, image: Image.Image, score_threshold: float):
        encoding = self.processor(images=image, return_tensors="pt")
        pixel_values = encoding["pixel_values"].to(self.device)

        with torch.no_grad():
            outputs = self.model(pixel_values=pixel_values)

        target_sizes = torch.tensor([[image.height, image.width]], device=self.device)
        results = self.processor.post_process_object_detection(
            outputs, threshold=score_threshold, target_sizes=target_sizes
        )[0]

        boxes = results["boxes"].cpu().tolist()
        scores = results["scores"].cpu().tolist()
        labels = results["labels"].cpu().tolist()

        formatted = []
        for box, score, label in zip(boxes, scores, labels):
            class_index = int(label)
            if class_index < 0 or class_index >= len(self.class_names):
                continue
            formatted.append(
                {
                    "class": self.class_names[class_index],
                    "confidence": float(score),
                    "box": [float(x) for x in box],
                }
            )
        return formatted
