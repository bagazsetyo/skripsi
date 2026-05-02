from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parent
DATA_DIR = REPO_ROOT / "data" / "traffic_sign"
MODEL_DIR = PROJECT_ROOT / "models" / "yolos"
MODEL_PATH = MODEL_DIR

CLASS_NAMES = ["larangan-berhenti", "larangan-memutar-balik"]
SCORE_THRESHOLD = float(os.getenv("SCORE_THRESHOLD", "0.5"))
