# Improvisasi Model YOLOS - Deteksi Rambu Lalu Lintas

Dokumen ini mencatat daftar improvisasi yang akan dilakukan satu per satu untuk meningkatkan performa model.
Setiap improvisasi memiliki status, deskripsi masalah, dan file yang diubah.

---

## Status Ringkasan

| # | Improvisasi | Status | File Utama |
|---|-------------|--------|-----------|
| 1 | Augmentasi Data | ✅ Selesai | `backend/dataset.py` |
| 2 | Gradient Clipping | ✅ Selesai | `backend/training_core.py` |
| 3 | LR Warmup + Cosine Decay | ✅ Selesai | `backend/training_service.py`, `backend/app/schemas.py`, `colab/experiment_runner.py` |
| 4 | Turunkan Score Threshold Default | ✅ Selesai | `backend/config.py`, `backend/app/schemas.py` |
| 5 | Update Colab Presets | ✅ Selesai | `colab/experiment_runner.py` |
| 6 | Confusion Matrix di Evaluasi | ✅ Selesai | `backend/evaluation.py` |

---

## Improvisasi 1 — Augmentasi Data

**Status:** ✅ Selesai

### Masalah
`backend/dataset.py` tidak menerapkan augmentasi apapun. Gambar dari dataset Kaggle langsung
dipakai tanpa transformasi. Akibatnya:
- Model overfit ke kondisi gambar training (pencahayaan, warna, kontras tetap).
- Performa drop saat diuji di kondisi berbeda (video outdoor, kamera berbeda, cuaca).

### Solusi
Tambahkan augmentasi **hanya untuk split training** di `TrafficSignDataset.__getitem__`.
Augmentasi yang dipilih adalah yang **tidak mengubah posisi bounding box**:
- `ColorJitter` — variasikan brightness, contrast, saturation, hue
- `RandomGrayscale` — 10% chance dikonversi grayscale (bantu robustness terhadap warna)
- `GaussianBlur` — 30% chance blur ringan (simulasi kamera blur / jarak jauh)

Augmentasi spatial (flip, rotate, crop) **tidak dipakai** karena memerlukan transformasi ulang
koordinat bounding box, dan horizontal flip berbahaya untuk rambu arah
(contoh: "larangan-belok-kanan" bisa jadi mirip "larangan-belok-kiri" setelah diflip).

### File Diubah
- `backend/dataset.py`

---

## Improvisasi 2 — Gradient Clipping

**Status:** ✅ Selesai

### Masalah
`backend/training_core.py` tidak memiliki gradient clipping. Model YOLOS berbasis Vision
Transformer sangat rentan terhadap **exploding gradient**, terutama di awal training saat
head detection belum stabil. Tanpa clipping, loss bisa melonjak tiba-tiba.

### Solusi
Tambahkan `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.1)` sebelum
`optimizer.step()` di fungsi `train_one_epoch`.

Nilai `max_norm=0.1` adalah standar untuk fine-tuning DETR/YOLOS dari paper aslinya.

### File Diubah
- `backend/training_core.py`

---

## Improvisasi 3 — LR Warmup + Cosine Decay

**Status:** ✅ Selesai

### Masalah
Scheduler saat ini hanya `StepLR` yang menurunkan LR secara kasar setiap N epoch.
Tanpa **warmup**, attention head ViT bisa destabilize di epoch pertama karena langsung
menerima LR penuh. Tanpa **cosine decay**, penurunan LR terlalu abrupt.

### Solusi
Tambahkan dua parameter baru:
- `warmup_epochs` — berapa epoch pertama LR dinaikkan secara linear dari `lr_min` ke `lr`
- `cosine_decay` — flag untuk menggunakan cosine annealing setelah warmup

Jika `warmup_epochs > 0` dan `cosine_decay=True`, scheduler otomatis dibuat sebagai
`LinearWarmup → CosineAnnealingLR`. `StepLR` tetap bisa dipakai jika `warmup_epochs=0`.

### File Diubah
- `backend/training_service.py`
- `backend/training_core.py`
- `backend/app/schemas.py`
- `colab/experiment_runner.py`

---

## Improvisasi 4 — Turunkan Score Threshold Default

**Status:** ✅ Selesai

### Masalah
Default `SCORE_THRESHOLD = 0.5` terlalu tinggi untuk model yang belum mature.
YOLOS menggunakan Hungarian matching loss — confidence score-nya cenderung lebih rendah
dibanding YOLO konvensional. Banyak deteksi valid yang tersaring karena score 0.3–0.49.

### Solusi
Turunkan default menjadi `0.3`. Nilai ini masih cukup selektif untuk menekan false positive,
tapi tidak terlalu agresif menyaring true positive.

### File Diubah
- `backend/config.py`

---

## Improvisasi 5 — Update Colab Presets

**Status:** ✅ Selesai

### Masalah
Preset eksperimen di `colab/experiment_runner.py` belum mencerminkan improvisasi yang
sudah dikerjakan (gradient clipping, warmup, score threshold baru). Tanpa update,
training di Colab tidak akan memakai perbaikan tersebut.

### Solusi
Update `ExperimentPreset` dataclass dan semua preset (`img500`, `img600`, `img700`) untuk
menyertakan improvement baru dan dioptimalkan untuk **GPU L4 (24GB VRAM)**:

| Preset | image_size | batch_size | epochs | VRAM est. | Catatan |
|--------|-----------|-----------|--------|-----------|---------|
| img500 | 500 | 4 | 50 | ~15 GB | Cepat, cocok eksperimen awal |
| img600 | 600 | 2 | 40 | ~15 GB | Sweet spot detail vs kecepatan |
| img700 | 700 | 1 | 40 | ~13 GB | Resolusi terbaik untuk detail rambu |

Dasar perhitungan batch_size: VRAM skala O(tokens²) karena attention. Referensi 13 GB dari
laporan pengguna pada T4 (batch_size=1). L4 batas aman 80% = ~19 GB.

Parameter lain yang diupdate:
- `warmup_epochs` proporsional dengan epochs (~10%): 5 / 4 / 4
- `cosine_decay: True`, `grad_clip: 0.1`, `score_threshold: 0.3`
- `num_workers: 4` (dari 2) — L4 di Colab memiliki lebih banyak CPU core

### File Diubah
- `colab/experiment_runner.py`

---

---

## Improvisasi 6 — Confusion Matrix di Evaluasi

**Status:** ✅ Selesai

### Masalah
`backend/evaluation.py` hanya menghasilkan metrik per kelas (AP, precision, recall) tetapi
**tidak menunjukkan kelas mana yang salah diklasifikasikan menjadi kelas apa**. Ini membuat
diagnosis konfusi antar-kelas yang mirip visual (contoh: `larangan-belok-kiri` vs
`larangan-memutar-balik`) sangat sulit — kita hanya tahu ada FP/FN, bukan dari mana asalnya.

### Akar Masalah Konfusi Belok Kiri vs Memutar Balik
Kedua rambu ini sangat mirip secara visual:
- Keduanya lingkaran merah dengan panah ke arah kiri dan garis larangan diagonal
- Perbedaan hanya di **bentuk panah**: belok kiri = curve sederhana, memutar balik = huruf U
- Ketika rambu kecil di frame atau foto jarak jauh, bagian atas huruf U sering tidak terlihat
- `yolos-tiny` (6M parameter) tidak punya kapasitas yang cukup untuk membedakan detail kurva ini

Model id=10 (aktif) sudah pakai semua improvement kita, namun:
- `larangan-memutar-balik`: FN=8/30 (26.7% kelewatan)
- `larangan-belok-kiri`: FP=9 (kemungkinan besar ini adalah memutar-balik yang salah kelas)

Tanpa confusion matrix, kita tidak bisa **membuktikan** arah konfusinya secara kuantitatif.

### Solusi
Tambahkan `confusion_matrix` ke output `evaluate_model`. Confusion matrix yang dihasilkan adalah
matrix N×N (N = jumlah kelas) di mana:
- Baris = kelas prediksi
- Kolom = kelas ground truth
- Nilai = jumlah prediksi yang cocok (TP match) per pasangan kelas

Ini berbeda dari confusion matrix klasifikasi biasa karena ini object detection — satu prediksi
di-match ke satu GT box berdasarkan IoU, sehingga kita bisa tahu "prediksi A sebenarnya GT B".

### File Diubah
- `backend/evaluation.py`

### Langkah Selanjutnya Jika Konfusi Masih Tinggi
Jika setelah retrain dengan semua improvement confusion matrix masih menunjukkan konfusi tinggi
antara kelas-kelas mirip, lakukan salah satu dari ini:

1. **Naik ke `yolos-small`** — ganti `DEFAULT_TRAIN_MODEL_NAME = "hustvl/yolos-small"` di
   `backend/config.py`. Model small punya 22M parameter (vs 6M tiny), jauh lebih baik untuk
   membedakan fitur detail seperti bentuk kurva panah. Butuh VRAM lebih besar (~6 GB).

2. **Naikkan image size ke 700** — gunakan preset `img700` di Colab. Resolusi lebih tinggi
   membantu model melihat detail kurva panah yang lebih jelas.

3. **Tambah data** — cari gambar yang lebih beragam untuk kelas yang sering salah. Pastikan
   variasi jarak, sudut, dan pencahayaan cukup.

---

## Catatan Umum

### Mengapa Tidak Ganti Model ke `yolos-small`?
`yolos-small` memiliki kapasitas lebih besar dan bisa meningkatkan akurasi, tetapi:
- Membutuhkan lebih banyak VRAM (min ~6 GB untuk batch_size=1 di image_size=512)
- Waktu training 2–3× lebih lama
- Lebih baik perbaiki pipeline training dulu, baru scale model jika hasilnya masih kurang

Ganti ke `yolos-small` bisa dilakukan dengan mengubah `DEFAULT_TRAIN_MODEL_NAME` di
`backend/config.py` atau lewat parameter `--model-name` di Colab runner.

### Urutan Perbaikan
Perbaikan 1–5 di atas harus dikerjakan berurutan karena Colab presets (improvisasi 5)
bergantung pada skema baru yang ditambahkan di improvisasi 3.
