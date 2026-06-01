from __future__ import annotations

import argparse
import queue
import threading
import time
from dataclasses import dataclass, field

from PIL import Image
import torch

from app.inference import Predictor
from config import CLASS_NAMES, SCORE_THRESHOLD
from model_registry import ensure_default_model_registered, resolve_active_model_path

try:
    import cv2
except ImportError as exc:  # pragma: no cover - runtime dependency guard
    raise SystemExit(
        "OpenCV belum terpasang. Install dependency backend dulu, termasuk opencv-python."
    ) from exc


@dataclass
class SharedDetectionState:
    detections: list[dict] = field(default_factory=list)
    processing: bool = False
    inference_ms: float = 0.0
    updated_at: float | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deteksi near real-time YOLOS menggunakan kamera/video via OpenCV."
    )
    parser.add_argument("--camera-index", type=int, default=0, help="Index kamera OpenCV.")
    parser.add_argument(
        "--video",
        type=str,
        default="",
        help="Path file video. Jika kosong, sistem memakai kamera.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.5,
        help="Interval inferensi dalam detik. Default 0.5 detik.",
    )
    parser.add_argument(
        "--score-threshold",
        type=float,
        default=SCORE_THRESHOLD,
        help="Threshold confidence prediksi.",
    )
    parser.add_argument(
        "--window-name",
        type=str,
        default="YOLOS Real-Time Demo",
        help="Nama window OpenCV.",
    )
    parser.add_argument(
        "--display-width",
        type=int,
        default=1280,
        help="Lebar target tampilan window. 0 untuk ukuran asli frame.",
    )
    return parser.parse_args()


def resolve_predictor() -> tuple[Predictor, dict]:
    ensure_default_model_registered()
    active_model, model_path = resolve_active_model_path()
    if active_model is None or model_path is None:
        raise SystemExit("Model aktif tidak ditemukan. Pastikan model YOLOS sudah tersedia.")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    predictor = Predictor(model_path, active_model["class_names"] or CLASS_NAMES, device)
    return predictor, active_model


def update_processing_state(shared_state: SharedDetectionState, state_lock: threading.Lock, value: bool) -> None:
    with state_lock:
        shared_state.processing = value


def run_inference_worker(
    predictor: Predictor,
    frame_queue: queue.Queue,
    shared_state: SharedDetectionState,
    state_lock: threading.Lock,
    stop_event: threading.Event,
    score_threshold: float,
) -> None:
    while not stop_event.is_set():
        try:
            frame = frame_queue.get(timeout=0.1)
        except queue.Empty:
            continue

        update_processing_state(shared_state, state_lock, True)
        started = time.perf_counter()

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_frame)
        detections = predictor.predict(image, score_threshold=score_threshold)
        inference_ms = (time.perf_counter() - started) * 1000

        with state_lock:
            shared_state.detections = detections
            shared_state.inference_ms = inference_ms
            shared_state.updated_at = time.time()
            shared_state.processing = False

        frame_queue.task_done()


def enqueue_latest_frame(frame_queue: queue.Queue, frame) -> None:
    try:
        frame_queue.put_nowait(frame)
        return
    except queue.Full:
        pass

    try:
        frame_queue.get_nowait()
        frame_queue.task_done()
    except queue.Empty:
        pass

    try:
        frame_queue.put_nowait(frame)
    except queue.Full:
        # Kondisi balapan kecil bisa terjadi. Jika masih penuh, abaikan saja.
        pass


def draw_detection_overlay(frame, detections: list[dict]) -> None:
    for item in detections:
        x1, y1, x2, y2 = [int(value) for value in item["box"]]
        label = item["class"]
        confidence = item["confidence"] * 100
        color = (0, 200, 0)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        text = f"{label} {confidence:.1f}%"
        (text_width, text_height), _ = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
        )
        text_y = max(y1, text_height + 10)
        cv2.rectangle(
            frame,
            (x1, text_y - text_height - 8),
            (x1 + text_width + 10, text_y),
            color,
            -1,
        )
        cv2.putText(
            frame,
            text,
            (x1 + 5, text_y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (10, 20, 10),
            1,
            cv2.LINE_AA,
        )


def draw_status_overlay(
    frame,
    *,
    fps: float,
    inference_ms: float,
    processing: bool,
    model_label: str,
    detection_count: int,
) -> None:
    lines = [
        f"Model: {model_label}",
        f"FPS: {fps:.1f}",
        f"Deteksi terakhir: {detection_count} objek",
        f"Inferensi: {inference_ms:.1f} ms",
    ]

    if processing:
        lines.append("Processing...")

    block_width = 330
    block_height = 28 + (len(lines) * 28)
    cv2.rectangle(frame, (16, 16), (16 + block_width, 16 + block_height), (15, 23, 42), -1)

    for index, line in enumerate(lines):
        y = 48 + (index * 28)
        color = (255, 255, 255)
        if line == "Processing...":
            color = (80, 220, 255)
        cv2.putText(
            frame,
            line,
            (30, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2,
            cv2.LINE_AA,
        )


def resize_for_display(frame, display_width: int):
    if display_width <= 0:
        return frame

    height, width = frame.shape[:2]
    if width <= display_width:
        return frame

    scale = display_width / float(width)
    target_height = int(height * scale)
    return cv2.resize(frame, (display_width, target_height), interpolation=cv2.INTER_AREA)


def main() -> None:
    args = parse_args()
    predictor, active_model = resolve_predictor()

    source = args.video if args.video else args.camera_index
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise SystemExit("Gagal membuka kamera atau file video.")

    frame_queue: queue.Queue = queue.Queue(maxsize=1)
    state_lock = threading.Lock()
    stop_event = threading.Event()
    shared_state = SharedDetectionState()

    worker = threading.Thread(
        target=run_inference_worker,
        args=(
            predictor,
            frame_queue,
            shared_state,
            state_lock,
            stop_event,
            args.score_threshold,
        ),
        daemon=True,
    )
    worker.start()

    window_name = args.window_name
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    last_enqueue_at = 0.0
    last_loop_at = time.perf_counter()
    fps = 0.0

    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                if args.video:
                    break
                continue

            now = time.perf_counter()
            loop_delta = max(now - last_loop_at, 1e-6)
            fps = 1.0 / loop_delta
            last_loop_at = now

            if now - last_enqueue_at >= max(args.interval, 0.05):
                enqueue_latest_frame(frame_queue, frame.copy())
                last_enqueue_at = now

            with state_lock:
                detections = list(shared_state.detections)
                inference_ms = shared_state.inference_ms
                processing = shared_state.processing

            display_frame = frame.copy()
            draw_detection_overlay(display_frame, detections)
            draw_status_overlay(
                display_frame,
                fps=fps,
                inference_ms=inference_ms,
                processing=processing,
                model_label=active_model["display_name"],
                detection_count=len(detections),
            )

            display_frame = resize_for_display(display_frame, args.display_width)
            cv2.imshow(window_name, display_frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break
    finally:
        stop_event.set()
        capture.release()
        cv2.destroyAllWindows()
        worker.join(timeout=1.0)


if __name__ == "__main__":
    main()
