import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parent

DATA_ROOT = Path(os.getenv("DATA_ROOT", REPO_ROOT / "data"))
DATA_DIR = DATA_ROOT / "traffic_sign"
TRAIN_DIR = DATA_DIR / "train"
TEST_DIR = DATA_DIR / "test"

MODELS_ROOT = Path(os.getenv("MODELS_ROOT", PROJECT_ROOT / "models"))
MODEL_NAME = os.getenv("MODEL_NAME", "yolos")
MODEL_DIR = MODELS_ROOT / MODEL_NAME
MODEL_PATH = MODEL_DIR

CLASS_NAMES = [
    "larangan-berhenti",
    "larangan-masuk-bagi-kendaraan-bermotor-dan-tidak-bermotor",
    "larangan-parkir",
    "lampu-hijau",
    "lampu-kuning",
    "lampu-merah",
    "larangan-belok-kanan",
    "larangan-belok-kiri",
    "larangan-berjalan-terus-wajib-berhenti-sesaat",
    "larangan-memutar-balik",
    "peringatan-alat-pemberi-isyarat-lalu-lintas",
    "peringatan-banyak-pejalan-kaki-menggunakan-zebra-cross",
    "peringatan-pintu-perlintasan-kereta-api",
    "peringatan-simpang-tiga-sisi-kiri",
    "peringatan-penegasan-rambu-tambahan",
    "perintah-masuk-jalur-kiri",
    "perintah-pilihan-memasuki-salah-satu-jalur",
    "petunjuk-area-parkir",
    "petunjuk-lokasi-pemberhentian-bus",
    "petunjuk-lokasi-putar-balik",
    "petunjuk-penyeberangan-pejalan-kaki",
]

SCORE_THRESHOLD = float(os.getenv("SCORE_THRESHOLD", "0.5"))
