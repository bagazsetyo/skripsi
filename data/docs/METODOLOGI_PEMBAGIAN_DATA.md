# Metodologi Pembagian Data Training dan Testing

## 1. Sumber Data

Data yang digunakan dalam penelitian ini merupakan gambar rambu lalu lintas Indonesia
yang dikumpulkan dari beberapa sumber:

- **Dataset publik (Roboflow Universe)** — beberapa arsip dataset rambu lalu lintas
  Indonesia yang tersedia secara bebas, diolah ulang agar sesuai dengan kebutuhan
  penelitian
- **Data tambahan mandiri** — gambar yang dikumpulkan dan dianotasi secara manual
  menggunakan alat anotasi yang dikembangkan sebagai bagian dari sistem ini

Seluruh data disimpan dalam format **YOLO Label Format**:
satu gambar (`.jpg`) berpasangan dengan satu file label (`.txt`) berisi baris-baris:
```
class_id cx cy w h
```
di mana `cx cy w h` adalah koordinat bounding box yang dinormalisasi terhadap ukuran gambar
(nilai 0.0–1.0).

---

## 2. Jumlah Data dan Distribusi Kelas

| Split | Jumlah Gambar | Keterangan |
|-------|--------------|------------|
| **Train** | 5.494 | Variasi per kelas: 213–343 gambar |
| **Test**  | 540   | Seragam: tepat 30 gambar per kelas |
| **Total** | 6.034 | 18 kelas aktif |

### Distribusi per Kelas (Train)

| No | Label | Train | Test |
|----|-------|-------|------|
| 0  | larangan-berhenti | 327 | 30 |
| 1  | larangan-masuk-bagi-kendaraan-bermotor-dan-tidak-bermotor | 328 | 30 |
| 2  | larangan-parkir | 324 | 30 |
| 3  | larangan-belok-kanan | 331 | 30 |
| 4  | larangan-belok-kiri | 213 | 30 |
| 5  | larangan-berjalan-terus-wajib-berhenti-sesaat | 331 | 30 |
| 6  | larangan-memutar-balik | 301 | 30 |
| 7  | peringatan-alat-pemberi-isyarat-lalu-lintas | 333 | 30 |
| 8  | peringatan-banyak-pejalan-kaki-menggunakan-zebra-cross | 239 | 30 |
| 9  | peringatan-pintu-perlintasan-kereta-api | 237 | 30 |
| 10 | peringatan-simpang-tiga-sisi-kiri | 250 | 30 |
| 11 | peringatan-penegasan-rambu-tambahan | 328 | 30 |
| 12 | perintah-masuk-jalur-kiri | 343 | 30 |
| 13 | perintah-pilihan-memasuki-salah-satu-jalur | 332 | 30 |
| 14 | petunjuk-area-parkir | 332 | 30 |
| 15 | petunjuk-lokasi-pemberhentian-bus | 309 | 30 |
| 16 | petunjuk-lokasi-putar-balik | 305 | 30 |
| 17 | petunjuk-penyeberangan-pejalan-kaki | 331 | 30 |

> Data terakhir diperbarui dari folder aktual `data/traffic_sign/train`.
> Total train 5.494 gambar, min 213 (larangan-belok-kiri), maks 343 (perintah-masuk-jalur-kiri).

---

## 3. Metode Pembagian Data — Stratified Sampling

Pembagian data menggunakan metode **Stratified Sampling** (pengambilan sampel
berstrata), yaitu setiap kelas direpresentasikan secara proporsional pada data test.

### Cara Kerja

1. Untuk setiap kelas, **30 gambar disisihkan secara tetap** sebagai data test
2. Seluruh gambar sisanya digunakan sebagai data train
3. Proses ini memastikan bahwa **setiap kelas selalu terwakili** di data test,
   tanpa ada kelas yang tidak teruji sama sekali

### Mengapa Stratified (bukan Random Biasa)?

| Metode | Kelebihan | Kekurangan |
|--------|-----------|-----------|
| **Random Sampling** | Sederhana | Kelas dengan data sedikit bisa tidak muncul di test set |
| **Stratified Sampling** | Setiap kelas pasti terwakili di test | Sedikit lebih kompleks |

Untuk dataset deteksi objek dengan **18 kelas** dan distribusi 213–343 gambar
per kelas, stratified sampling dipilih agar evaluasi adil untuk semua kelas.

---

## 4. Rasio Train : Test

| | Jumlah | Persentase |
|-|--------|-----------|
| Train | 5.494 | **91%** |
| Test  | 540   | **9%**  |
| Total | 6.034 | 100% |

**Rasio aktual: ≈ 91 : 9**

### Penjelasan untuk Dosen (Jika Ditanya Kenapa Bukan 80:20)

Rasio 91:9 muncul bukan karena dipilih secara acak, melainkan sebagai **konsekuensi
dari stratified sampling dengan fixed test size (30 per kelas)**:

- 18 kelas × 30 gambar = **540 gambar test** (nilai tetap)
- Sisa data → train
- Karena jumlah data train terus bertambah (dari berbagai sumber), persentase test
  otomatis mengecil mendekati 9%

**Justifikasi ilmiah:**
> Dalam penelitian computer vision, rasio 80:20 adalah panduan umum, bukan aturan
> mutlak. Dengan jumlah data test yang fixed (30 per kelas × 18 kelas = 540 sampel)
> dan distribusi yang seragam antar kelas, kualitas evaluasi tetap terjamin meskipun
> persentase test kurang dari 20%. Pendekatan ini juga digunakan dalam benchmark
> dataset seperti PASCAL VOC yang mempertahankan test set tetap untuk konsistensi
> evaluasi lintas eksperimen.

**Intinya untuk dijawab:** "Kami menggunakan stratified sampling dengan 30 sampel
per kelas di test set untuk memastikan evaluasi yang adil dan merata antar kelas,
sesuai dengan praktik umum dalam riset deteksi objek multi-kelas."

---

## 5. Di Mana Training Dilakukan

| Tahap | Lokasi | Keterangan |
|-------|--------|-----------|
| **Pengumpulan & anotasi data** | Lokal (laptop) | Menggunakan tools yang dikembangkan di sistem ini |
| **Training model** | Google Colab (cloud) | GPU NVIDIA A100 80 GB |
| **Evaluasi / testing** | Google Colab (cloud) | Dijalankan otomatis setiap akhir epoch |
| **Inferensi / deployment** | Lokal (server FastAPI) | Model hasil training di-download dan diaktifkan |

### Alasan Training di Cloud

Model YOLOS-small adalah arsitektur **Vision Transformer** yang membutuhkan GPU
dengan VRAM besar. Training di laptop (CPU atau GPU laptop) akan:
- Sangat lambat: estimasi 10–50× lebih lambat dari A100
- Tidak praktis untuk iterasi eksperimen

Google Colab dipilih karena menyediakan akses GPU kelas atas (A100 80 GB) dengan
biaya yang terjangkau untuk kebutuhan penelitian skripsi.

---

## 6. Alur Keseluruhan (Pipeline)

```
Sumber data (Roboflow + mandiri)
        ↓
Anotasi & kurasi (tools lokal)
        ↓
Dataset YOLO format (data/traffic_sign/)
        ↓
Upload ke Google Drive → zip (traffic_sign.zip)
        ↓
Training di Google Colab (A100 GPU)
    ├── small-img500  (40 epoch, bs=2)
    ├── small-img600  (40 epoch, bs=2)
    └── small-img700  (40 epoch, bs=2)
        ↓
Model terbaik (.zip) di-download
        ↓
Import ke sistem via /models/import
        ↓
Evaluasi & inferensi via /video-demo
```

---

## 7. Metode Training (Untuk Jawaban ke Dosen)

**"Training menggunakan apa?"**

| Aspek | Metode | Keterangan |
|-------|--------|-----------|
| **Arsitektur** | Vision Transformer (ViT) | YOLOS-small dari HuggingFace |
| **Optimizer** | AdamW | Varian Adam dengan weight decay terpisah |
| **Loss Function** | Hungarian Matching Loss | Dari arsitektur DETR; mencocokkan prediksi dengan ground truth secara optimal |
| **LR Scheduler** | Warmup + Cosine Decay | LR naik bertahap lalu turun mengikuti kurva kosinus |
| **Regularisasi** | Weight Decay + Gradient Clipping | Mencegah overfitting dan exploding gradient |
| **Augmentasi** | ColorJitter, GaussianBlur, RandomGrayscale | Diterapkan hanya pada data train |
| **Presisi** | Mixed Precision (AMP) | FP16 untuk komputasi, FP32 untuk akumulasi gradient |

**"Perbandingannya berapa banding berapa?"**
> Train : Test = **91% : 9%** menggunakan metode **Stratified Sampling**,
> dengan 30 gambar per kelas pada data test (total 540 gambar) untuk memastikan
> evaluasi yang merata di semua 18 kelas.
