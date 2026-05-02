import os
from dataclasses import dataclass
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
REGISTRY_DB_PATH = Path(os.getenv("REGISTRY_DB_PATH", PROJECT_ROOT / "app.db"))
DEFAULT_TRAIN_MODEL_NAME = os.getenv("DEFAULT_TRAIN_MODEL_NAME", "hustvl/yolos-tiny")
DEFAULT_IMAGE_SIZE = int(os.getenv("DEFAULT_IMAGE_SIZE", "512"))
DEFAULT_BATCH_SIZE = int(os.getenv("DEFAULT_BATCH_SIZE", "1"))
DEFAULT_EPOCHS = int(os.getenv("DEFAULT_EPOCHS", "30"))
DEFAULT_LEARNING_RATE = float(os.getenv("DEFAULT_LEARNING_RATE", "1e-4"))
DEFAULT_WEIGHT_DECAY = float(os.getenv("DEFAULT_WEIGHT_DECAY", "1e-4"))


@dataclass(frozen=True)
class TrafficSignClass:
    class_id: int
    label: str
    directory: str


TRAFFIC_SIGN_CLASSES = [
    TrafficSignClass(0, "larangan-berhenti", "larangan-berhenti"),
    TrafficSignClass(
        1,
        "larangan-masuk-bagi-kendaraan-bermotor-dan-tidak-bermotor",
        "larangan-masuk-bagi-kendaraan-bermotor-dan-tidak-bermotor",
    ),
    TrafficSignClass(2, "larangan-parkir", "larangan-parkir"),
    TrafficSignClass(3, "lampu-hijau", "lampu-hijau"),
    TrafficSignClass(4, "lampu-kuning", "lampu-kuning"),
    TrafficSignClass(5, "lampu-merah", "lampu-merah"),
    TrafficSignClass(6, "larangan-belok-kanan", "larangan-belok-kanan"),
    TrafficSignClass(7, "larangan-belok-kiri", "larangan-belok-kiri"),
    TrafficSignClass(
        8,
        "larangan-berjalan-terus-wajib-berhenti-sesaat",
        "larangan-berjalan-terus-wajib-berhenti-sesaat",
    ),
    TrafficSignClass(9, "larangan-memutar-balik", "larangan-memutar-balik"),
    TrafficSignClass(
        10,
        "peringatan-alat-pemberi-isyarat-lalu-lintas",
        "peringatan-alat-pemberi-isyarat-lalu-lintas",
    ),
    TrafficSignClass(
        11,
        "peringatan-banyak-pejalan-kaki-menggunakan-zebra-cross",
        "peringatan-banyak-pejalan-kaki-menggunakan-zebra-cross",
    ),
    TrafficSignClass(
        12,
        "peringatan-pintu-perlintasan-kereta-api",
        "peringatan-pintu-perlintasan-kereta-api",
    ),
    TrafficSignClass(
        13,
        "peringatan-simpang-tiga-sisi-kiri",
        "peringatan-simpang-tiga-sisi-kiri",
    ),
    TrafficSignClass(
        14,
        "peringatan-penegasan-rambu-tambahan",
        "peringatan-penegasan-rambu-tambahan",
    ),
    TrafficSignClass(15, "perintah-masuk-jalur-kiri", "perintah-masuk-jalur-kiri"),
    TrafficSignClass(
        16,
        "perintah-pilihan-memasuki-salah-satu-jalur",
        "perintah-pilihan-memasuki-salah-satu-jalur",
    ),
    TrafficSignClass(17, "petunjuk-area-parkir", "petunjuk-area-parkir"),
    TrafficSignClass(
        18,
        "petunjuk-lokasi-pemberhentian-bus",
        "petunjuk-lokasi-pemberhentian-bus",
    ),
    TrafficSignClass(
        19,
        "petunjuk-lokasi-putar-balik",
        "petunjuk-lokasi-putar-balik",
    ),
    TrafficSignClass(
        20,
        "petunjuk-penyeberangan-pejalan-kaki",
        "petunjuk-penyeberangan-pejalan-kaki",
    ),
]

CLASS_NAMES = [item.label for item in TRAFFIC_SIGN_CLASSES]
CLASS_DIRECTORIES = [item.directory for item in TRAFFIC_SIGN_CLASSES]
CLASS_IDS = [item.class_id for item in TRAFFIC_SIGN_CLASSES]

CLASS_ID_TO_LABEL = {item.class_id: item.label for item in TRAFFIC_SIGN_CLASSES}
CLASS_ID_TO_DIRECTORY = {item.class_id: item.directory for item in TRAFFIC_SIGN_CLASSES}
CLASS_LABEL_TO_ID = {item.label: item.class_id for item in TRAFFIC_SIGN_CLASSES}
CLASS_DIRECTORY_TO_ID = {
    item.directory: item.class_id for item in TRAFFIC_SIGN_CLASSES
}
CLASS_DIRECTORY_TO_LABEL = {
    item.directory: item.label for item in TRAFFIC_SIGN_CLASSES
}
CLASS_LABEL_TO_DIRECTORY = {
    item.label: item.directory for item in TRAFFIC_SIGN_CLASSES
}

SCORE_THRESHOLD = float(os.getenv("SCORE_THRESHOLD", "0.5"))
