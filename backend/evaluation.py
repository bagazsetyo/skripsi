from __future__ import annotations

from collections import defaultdict
from typing import Any

import numpy as np
import torch
from transformers import YolosImageProcessor


def xywh_to_xyxy(box: list[float]) -> list[float]:
    x_min, y_min, width, height = box
    return [x_min, y_min, x_min + width, y_min + height]


def compute_iou(box_a: list[float], box_b: list[float]) -> float:
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])

    inter_w = max(0.0, x_b - x_a)
    inter_h = max(0.0, y_b - y_a)
    intersection = inter_w * inter_h
    if intersection <= 0:
        return 0.0

    area_a = max(0.0, box_a[2] - box_a[0]) * max(0.0, box_a[3] - box_a[1])
    area_b = max(0.0, box_b[2] - box_b[0]) * max(0.0, box_b[3] - box_b[1])
    union = area_a + area_b - intersection
    if union <= 0:
        return 0.0
    return intersection / union


def compute_average_precision(recalls: np.ndarray, precisions: np.ndarray) -> float:
    mrec = np.concatenate(([0.0], recalls, [1.0]))
    mpre = np.concatenate(([0.0], precisions, [0.0]))
    for idx in range(len(mpre) - 1, 0, -1):
        mpre[idx - 1] = max(mpre[idx - 1], mpre[idx])
    changing_points = np.where(mrec[1:] != mrec[:-1])[0]
    return float(np.sum((mrec[changing_points + 1] - mrec[changing_points]) * mpre[changing_points + 1]))


def evaluate_model(
    *,
    model,
    processor: YolosImageProcessor,
    dataset,
    class_names: list[str],
    device: torch.device,
    score_threshold: float = 0.5,
    iou_threshold: float = 0.5,
) -> dict[str, Any]:
    gt_by_image_class: dict[tuple[int, int], list[list[float]]] = defaultdict(list)
    gt_count_by_class: dict[int, int] = defaultdict(int)
    predictions_by_class: dict[int, list[dict[str, Any]]] = defaultdict(list)

    model.eval()
    with torch.no_grad():
        for image_index in range(len(dataset)):
            image, target = dataset[image_index]
            encoding = processor(images=image, return_tensors="pt")
            pixel_values = encoding["pixel_values"].to(device)
            outputs = model(pixel_values=pixel_values)
            target_sizes = torch.tensor([[image.height, image.width]], device=device)
            results = processor.post_process_object_detection(
                outputs,
                threshold=score_threshold,
                target_sizes=target_sizes,
            )[0]

            for annotation in target["annotations"]:
                class_id = int(annotation["category_id"])
                gt_box = xywh_to_xyxy(annotation["bbox"])
                gt_by_image_class[(image_index, class_id)].append(gt_box)
                gt_count_by_class[class_id] += 1

            for box, score, label in zip(
                results["boxes"].cpu().tolist(),
                results["scores"].cpu().tolist(),
                results["labels"].cpu().tolist(),
            ):
                class_id = int(label)
                predictions_by_class[class_id].append(
                    {
                        "image_id": image_index,
                        "score": float(score),
                        "box": [float(value) for value in box],
                    }
                )

    per_class_metrics: list[dict[str, Any]] = []
    ap_values: list[float] = []
    total_tp = 0
    total_fp = 0
    total_fn = 0

    for class_id, class_name in enumerate(class_names):
        predictions = sorted(
            predictions_by_class.get(class_id, []),
            key=lambda item: item["score"],
            reverse=True,
        )
        gt_total = gt_count_by_class.get(class_id, 0)
        matched_gt: dict[tuple[int, int], set[int]] = defaultdict(set)
        tp = np.zeros(len(predictions))
        fp = np.zeros(len(predictions))
        matched_ious: list[float] = []

        for idx, prediction in enumerate(predictions):
            key = (prediction["image_id"], class_id)
            gt_boxes = gt_by_image_class.get(key, [])
            best_iou = 0.0
            best_gt_index = -1
            for gt_index, gt_box in enumerate(gt_boxes):
                if gt_index in matched_gt[key]:
                    continue
                iou = compute_iou(prediction["box"], gt_box)
                if iou > best_iou:
                    best_iou = iou
                    best_gt_index = gt_index

            if best_iou >= iou_threshold and best_gt_index >= 0:
                tp[idx] = 1
                matched_gt[key].add(best_gt_index)
                matched_ious.append(best_iou)
            else:
                fp[idx] = 1

        tp_cumsum = np.cumsum(tp)
        fp_cumsum = np.cumsum(fp)
        recalls = tp_cumsum / gt_total if gt_total > 0 else np.zeros(len(predictions))
        precisions = tp_cumsum / np.maximum(tp_cumsum + fp_cumsum, 1e-12)
        ap = compute_average_precision(recalls, precisions) if gt_total > 0 else 0.0
        if gt_total > 0:
            ap_values.append(ap)

        class_tp = int(tp.sum())
        class_fp = int(fp.sum())
        class_fn = max(gt_total - class_tp, 0)
        total_tp += class_tp
        total_fp += class_fp
        total_fn += class_fn

        per_class_metrics.append(
            {
                "class_id": class_id,
                "class_name": class_name,
                "ground_truth_count": gt_total,
                "prediction_count": len(predictions),
                "true_positive": class_tp,
                "false_positive": class_fp,
                "false_negative": class_fn,
                "precision": class_tp / (class_tp + class_fp) if (class_tp + class_fp) else 0.0,
                "recall": class_tp / gt_total if gt_total else 0.0,
                "ap_50": ap,
                "mean_matched_iou": float(np.mean(matched_ious)) if matched_ious else 0.0,
            }
        )

    overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) else 0.0
    overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) else 0.0
    mean_iou = (
        float(np.mean([item["mean_matched_iou"] for item in per_class_metrics if item["true_positive"] > 0]))
        if any(item["true_positive"] > 0 for item in per_class_metrics)
        else 0.0
    )

    return {
        "iou_threshold": iou_threshold,
        "score_threshold": score_threshold,
        "ground_truth_total": sum(gt_count_by_class.values()),
        "prediction_total": sum(len(items) for items in predictions_by_class.values()),
        "true_positive": total_tp,
        "false_positive": total_fp,
        "false_negative": total_fn,
        "precision": overall_precision,
        "recall": overall_recall,
        "mAP_50": float(np.mean(ap_values)) if ap_values else 0.0,
        "mean_iou": mean_iou,
        "per_class": per_class_metrics,
    }
