# Panduan Revisi Skripsi — Bagas Setyo Nugroho
## Deteksi dan Klasifikasi Rambu Lalu Lintas Indonesia Menggunakan Vision Transformer

> Dokumen ini merangkum semua yang perlu diubah, ditambah, dan diuji
> berdasarkan catatan dosen dan kondisi sistem terkini.

---

## Ringkasan Perubahan Utama dari Draft UTA

| Aspek | Draft UTA (Lama) | Skripsi Final (Baru) |
|-------|-----------------|---------------------|
| Input sistem | Gambar statis yang diunggah | **Video real-time** (kamera/webcam) |
| Jumlah model yang dibandingkan | Belum ada (rencana) | **3 model** (img500, img600, img700) |
| Evaluasi mAP/IoU | "Tidak menjadi fokus" | **Menjadi fokus utama Bab 4** |
| Kelas lampu lalu lintas | Belum jelas | **Dikeluarkan** (bukan rambu, tapi sinyal) |
| Batasan image size | Belum disebutkan | **Maksimal 700px** (di atas itu rawan OOM) |
| Dataset | Kaggle (disebutkan) | **Roboflow + anotasi mandiri**, 18 kelas, 6.034 gambar |

---

## BAB 1 — PENDAHULUAN (Revisi)

### Yang Perlu Diubah

**1.2 Rumusan Masalah** — tambahkan poin:
- Bagaimana pengaruh ukuran gambar input (image size) terhadap akurasi deteksi
  rambu lalu lintas pada model YOLOS-small?
- Bagaimana mengimplementasikan sistem deteksi rambu secara real-time berbasis
  video menggunakan model YOLOS yang telah dilatih?

**1.3 Tujuan Penelitian** — tambahkan poin:
- Membandingkan performa tiga varian model YOLOS-small dengan image size
  berbeda (500, 600, 700 px) menggunakan metrik mAP@0.5, Precision, dan Recall.
- Mengimplementasikan sistem deteksi rambu lalu lintas secara real-time berbasis
  video/kamera pada antarmuka web.

**1.4 Batasan Masalah** — ubah poin 2 dan 7:
- ~~Input berupa gambar statis~~ → **Input berupa video real-time dari kamera atau
  file video yang diunggah**
- ~~Evaluasi mAP/IoU tidak menjadi fokus~~ → **Evaluasi kuantitatif menggunakan
  mAP@0.5, Precision, Recall, dan Mean IoU menjadi komponen utama Bab 4**
- Tambahkan: Ukuran gambar input dibatasi maksimal 700 px karena keterbatasan
  VRAM GPU (A100 80 GB) dengan batch size 2.
- Tambahkan: Dataset lampu lalu lintas (lampu-hijau, lampu-kuning, lampu-merah)
  tidak disertakan karena termasuk alat pemberi isyarat, bukan rambu lalu lintas
  sesuai PM 13 Tahun 2014.

---

## BAB 2 — LANDASAN TEORI (Revisi Minor)

### Yang Perlu Ditambahkan

**Subbab baru: Video Real-Time Detection**
Tambahkan penjelasan singkat (~1 halaman) tentang:
- Perbedaan deteksi pada gambar statis vs video/streaming
- Konsep frame-by-frame processing
- Tantangan real-time: latency, frame rate, konsistensi deteksi antar frame

**Subbab baru: Metrik Evaluasi Deteksi Objek**
Tambahkan penjelasan masing-masing metrik yang digunakan:
- **mAP@0.5** (Mean Average Precision pada IoU threshold 0.5) — metrik utama
- **Precision** — dari semua prediksi positif, berapa yang benar
- **Recall** — dari semua objek nyata, berapa yang berhasil terdeteksi
- **Mean IoU** — rata-rata Intersection over Union pada deteksi yang benar
- **Confusion Matrix** — visualisasi kelas mana yang sering tertukar

**Subbab 2.6 — Teknologi Pendukung** — tambahkan:
- WebSocket atau SSE (untuk streaming video ke frontend)
- OpenCV (untuk pemrosesan frame video)

---

## BAB 3 — PERANCANGAN (Revisi Signifikan)

### Yang Perlu Diubah

**3.2 Gambaran Umum Sistem**

Gambar alur sistem perlu diperbarui:
- Sebelumnya: `Pengguna → Upload Gambar → Prediksi → Hasil`
- Sekarang: `Kamera/Video → Frame Capture → Prediksi per Frame → Overlay Hasil → Display Real-time`

**3.3 Data Penelitian** — perbarui seluruhnya:

| Info | Nilai |
|------|-------|
| Sumber | Roboflow Universe + anotasi mandiri |
| Total gambar | 6.034 |
| Kelas aktif | 18 kelas rambu |
| Kelas dikeluarkan | 3 (lampu-hijau, lampu-kuning, lampu-merah) — alasan: bukan rambu |
| Data train | 5.494 gambar (91%) |
| Data test | 540 gambar (9%) — 30 per kelas, stratified sampling |
| Format anotasi | YOLO (.txt), bounding box ternormalisasi |

**3.4 Perancangan Metode** — tambahkan subbab baru:

### 3.4.1 Konfigurasi Eksperimen (BARU — WAJIB ADA per catatan dosen)

Jelaskan setiap hyperparameter beserta alasannya:

| Parameter | Nilai | Penjelasan |
|-----------|-------|-----------|
| **Image Size** | 500 / 600 / 700 px | Sisi terpanjang gambar setelah resize. Resolusi lebih tinggi menangkap lebih banyak detail, namun meningkatkan konsumsi VRAM dan waktu komputasi. |
| **Batch Size** | 2 | Jumlah gambar per langkah pembaruan bobot. Nilai 2 dipilih karena keterbatasan VRAM; lebih besar tidak memungkinkan pada image size 700px. |
| **Epochs** | 40 | Jumlah iterasi penuh melewati seluruh data training. Nilai 40 dipilih berdasarkan observasi konvergensi loss. |
| **Learning Rate** | 5×10⁻⁵ | Kecepatan pembaruan bobot model. Nilai kecil dipilih untuk fine-tuning model pretrained agar tidak merusak bobot awal. |
| **LR Warmup** | 4 epoch | LR dinaikkan bertahap selama 4 epoch pertama untuk stabilisasi training awal. |
| **LR Scheduler** | Cosine Decay | LR turun mengikuti kurva kosinus setelah warmup, mendorong konvergensi yang halus. |
| **Weight Decay** | 1×10⁻⁴ | Regularisasi L2 untuk mencegah overfitting. |
| **Gradient Clipping** | 0.1 | Membatasi besar gradient agar training stabil (penting untuk Transformer). |
| **Mixed Precision** | Ya (AMP) | Sebagian komputasi menggunakan FP16 untuk efisiensi memori dan kecepatan. |
| **GPU** | NVIDIA A100 80 GB | Diakses via Google Colab. |

### 3.4.2 Alasan Tiga Varian Image Size

Tuliskan alasan mengapa dipilih tiga varian:
- img500: baseline, efisien, VRAM ~35 GB
- img600: menengah, diharapkan menangkap lebih banyak detail rambu kecil
- img700: resolusi tertinggi yang memungkinkan dengan batch size 2; di atas ini
  VRAM ~46–50 GB dan rawan OOM jika batch size dipertahankan

### 3.4.3 Pembagian Data

Jelaskan stratified sampling:
- 30 gambar per kelas untuk test (fixed, bukan persentase)
- Alasan: menjamin evaluasi yang adil dan merata untuk semua 18 kelas
- Rasio 91:9 adalah konsekuensi, bukan tujuan

**3.6 Perancangan UML** — tambahkan/perbarui diagram:

- **Use Case Diagram** — tambahkan use case: `Deteksi via Video Real-time`
- **Activity Diagram** — tambahkan alur: `Buka Kamera → Capture Frame → Kirim ke Backend → Terima Hasil → Overlay Bounding Box → Tampilkan`
- **Sequence Diagram** — tambahkan sequence untuk prediksi video real-time

**3.7 Perancangan Antarmuka** — perbarui mockup:

- Ganti halaman "Prediksi" (upload gambar) menjadi halaman **"Video Demo"** yang
  menampilkan feed kamera dengan overlay bounding box secara real-time
- Tambahkan kontrol: play/pause, pilih model aktif, threshold slider

---

## BAB 4 — PENGUJIAN DAN IMPLEMENTASI (BAB BARU)

> Ini adalah bab yang paling banyak diisi setelah semua training selesai.
> Dosen meminta: **hasil perbandingan antar model ada di Bab 4**,
> bukan hanya narasi — harus ada tabel, grafik, dan analisis.

### 4.1 Lingkungan Pengujian

| Komponen | Spesifikasi |
|----------|------------|
| Training | Google Colab, GPU NVIDIA A100 80 GB |
| Inference (lokal) | [isi spesifikasi laptop/PC kamu] |
| Backend | FastAPI, Python 3.x |
| Frontend | React |
| OS | [isi OS kamu] |

### 4.2 Hasil Training

**4.2.1 Tabel Perbandingan Keseluruhan**

| Model | mAP@0.5 | Precision | Recall | Mean IoU | Waktu Training |
|-------|---------|-----------|--------|----------|----------------|
| YOLOS-small img500 | 90.27% | 89.79% | 91.23% | 90.67% | 8.77 jam |
| **YOLOS-small img600** | **92.07%** | **94.16%** | **92.31%** | 90.71% | 8.75 jam |
| YOLOS-small img700 | 90.83% | 92.24% | 91.41% | 91.22% | 8.78 jam |

**4.2.2 Tabel mAP per Kelas**

(Isi dari file `HASIL_PERBANDINGAN_MODEL.md` — sudah tersedia)

**4.2.3 Grafik Loss Training**

Buat grafik loss per epoch untuk ketiga model (data sudah ada di
`training_summary.json` masing-masing model → field `loss_history`).
Grafik ini menunjukkan konvergensi training.

**4.2.4 Analisis Confusion Matrix**

Fokus pada kelas yang sering tertukar:
- `larangan-memutar-balik` ↔ `larangan-parkir` (terjadi di semua model)
- `perintah-masuk-jalur-kiri` ↔ `perintah-pilihan-memasuki-salah-satu-jalur`
- Jelaskan: kedua pasang kelas ini memiliki kemiripan visual (bentuk/warna serupa)

### 4.3 Analisis Perbandingan Model

**4.3.1 Pengaruh Image Size terhadap mAP**

Tulis analisis: resolusi lebih tinggi tidak selalu lebih baik. img600 adalah titik optimal
pada dataset ini. img700 justru lebih buruk dari img600 karena terlalu banyak patch
membuat attention model terpecah pada kelas dengan kemiripan visual tinggi.

**4.3.2 Kelas yang Diuntungkan oleh Resolusi Tinggi**

| Kelas | img500 | img600 | img700 | Keterangan |
|-------|--------|--------|--------|-----------|
| larangan-parkir | 61.1% | 68.2% | 75.5% | Makin baik dengan resolusi tinggi |
| perintah-masuk-jalur-kiri | 72.3% | 81.7% | 89.2% | Butuh detail visual |

**4.3.3 Kelas yang Tidak Diuntungkan**

| Kelas | img500 | img600 | img700 | Keterangan |
|-------|--------|--------|--------|-----------|
| larangan-memutar-balik | 66.1% | 65.9% | 48.7% | img700 drop drastis |
| peringatan-alat-pemberi-isyarat | 99.6% | 96.6% | 90.0% | img500 justru terbaik |

**4.3.4 Model Terpilih**

YOLOS-small img600 dipilih sebagai model utama karena mAP tertinggi (92.07%),
precision terbaik (94.16%), dan performa paling seimbang di seluruh kelas.

### 4.4 Pengujian Sistem (Manual — Kamu yang Isi)

#### 4.4.1 Pengujian Fungsional

Uji semua fitur utama sistem dan catat hasilnya:

| No | Fitur yang Diuji | Langkah Uji | Hasil yang Diharapkan | Hasil Aktual | Status |
|----|-----------------|-------------|----------------------|-------------|--------|
| 1 | Deteksi video real-time | Buka halaman video demo, aktifkan kamera | Bounding box muncul di atas rambu dengan label dan confidence score | ... | ✓/✗ |
| 2 | Ganti model aktif | Pilih model berbeda dari dropdown | Model berganti, deteksi menggunakan model baru | ... | ✓/✗ |
| 3 | Deteksi multi-rambu | Tunjukkan 2 rambu berbeda di depan kamera | Keduanya terdeteksi dengan label yang benar | ... | ✓/✗ |
| 4 | Threshold confidence | Ubah slider threshold | Deteksi dengan confidence di bawah threshold hilang | ... | ✓/✗ |
| 5 | Upload video file | Upload file .mp4 | Deteksi berjalan frame by frame pada video | ... | ✓/✗ |
| 6 | Model management | Import model baru via /models/import | Model muncul di daftar, bisa diaktifkan | ... | ✓/✗ |
| 7 | Dataset validation | Buka halaman dataset | Tidak ada error (setelah perbaikan validator) | ... | ✓/✗ |

#### 4.4.2 Pengujian Performa Real-Time

Ukur dan catat:
- **Frame rate (FPS)** saat deteksi real-time dengan masing-masing model
- **Latency** dari frame masuk sampai hasil tampil (estimasi, bisa dari browser DevTools)
- **Akurasi visual** — apakah bounding box tepat menempel di rambu

| Model | FPS (estimasi) | Latency (ms) | Catatan |
|-------|---------------|-------------|---------|
| img500 | ... | ... | |
| img600 | ... | ... | |
| img700 | ... | ... | |

#### 4.4.3 Pengujian Kondisi Nyata

Uji dengan berbagai kondisi untuk menunjukkan ketahanan model:

| Kondisi | Rambu yang Diuji | Terdeteksi? | Confidence | Catatan |
|---------|-----------------|-------------|-----------|---------|
| Cahaya normal | larangan-berhenti | ... | ...% | |
| Cahaya redup/malam | larangan-berhenti | ... | ...% | |
| Sudut miring (~45°) | larangan-parkir | ... | ...% | |
| Jarak jauh | peringatan-simpang-tiga | ... | ...% | |
| Gambar buram/gerak | larangan-memutar-balik | ... | ...% | |
| 2 rambu sekaligus | bebas | ... | ...% | |

> **Catatan:** Untuk pengujian ini, kamu bisa menggunakan gambar rambu dari Google
> atau foto langsung. Tidak harus di jalan raya — di dalam ruangan dengan rambu
> yang dicetak pun valid untuk prototipe.

#### 4.4.4 Analisis Hasil Pengujian Nyata

Setelah pengujian, tulis analisis singkat:
- Kelas mana yang konsisten terdeteksi dengan baik
- Kelas mana yang sering gagal (terutama `larangan-memutar-balik`)
- Apakah kondisi cahaya mempengaruhi hasil secara signifikan
- Perbedaan performa real-time antar model (kecepatan vs akurasi)

### 4.5 Implementasi Antarmuka

Tampilkan screenshot antarmuka sistem yang sudah jadi:
- Dashboard
- Halaman Video Demo (deteksi real-time)
- Halaman Dataset
- Halaman Model Management

---

## BAB 5 — PENUTUP

### 5.1 Kesimpulan

Tulis 4–5 poin kesimpulan yang menjawab rumusan masalah:

1. **Model YOLOS-small berhasil dilatih** untuk mendeteksi dan mengklasifikasikan
   18 jenis rambu lalu lintas Indonesia dengan mAP@0.5 tertinggi 92.07%
   (img600), membuktikan bahwa Vision Transformer dapat diterapkan pada
   dataset rambu lalu lintas Indonesia.

2. **Pengaruh image size:** Image size 600 px menghasilkan performa terbaik.
   Peningkatan ke 700 px tidak memberikan peningkatan akurasi secara
   keseluruhan, mengindikasikan adanya titik optimal resolusi pada dataset ini.
   Perbedaan mAP antar ketiga model berkisar 1–2%, menunjukkan semua model
   sudah konvergen dengan baik.

3. **Sistem berbasis web berhasil diimplementasikan** dengan FastAPI (backend),
   React (frontend), dan SQLite (metadata model), mendukung deteksi rambu
   secara real-time melalui video/kamera dengan visualisasi bounding box langsung
   di antarmuka.

4. **Kelas dengan performa terendah** secara konsisten adalah `larangan-memutar-balik`
   (mAP tertinggi hanya 66.1% di img600), yang kemungkinan disebabkan
   kemiripan visual dengan `larangan-parkir` (keduanya berbentuk bulat merah).

5. **Pengujian fungsional** menunjukkan sistem dapat berjalan dengan baik pada
   kondisi [normal/variasi cahaya/dll — isi sesuai hasil pengujianmu].

### 5.2 Saran

1. **Peningkatan data kelas sulit:** Menambah data training untuk kelas
   `larangan-memutar-balik` dan `larangan-parkir` yang sering tertukar, serta
   menerapkan augmentasi data yang lebih agresif (rotasi, flip, brightness extremes)
   khusus untuk kelas-kelas tersebut.

2. **Eksplorasi arsitektur lain:** Membandingkan YOLOS dengan model deteksi
   berbasis CNN terbaru seperti YOLOv8/YOLOv9 untuk mendapatkan gambaran
   lebih lengkap tentang posisi Vision Transformer dalam ekosistem deteksi objek.

3. **Optimasi inferensi real-time:** Model saat ini belum dioptimasi untuk kecepatan
   inferensi. Teknik seperti model quantization (INT8) atau ONNX export dapat
   meningkatkan FPS secara signifikan untuk deployment di perangkat dengan
   GPU terbatas.

4. **Perluasan kelas:** Dataset dapat diperluas dengan kelas rambu tambahan
   (misalnya rambu kecepatan, rambu ukuran kendaraan) untuk meningkatkan
   cakupan sistem terhadap kondisi lalu lintas nyata di Indonesia.

5. **Pengujian di kondisi nyata:** Pengujian pada video dashcam atau CCTV jalan
   raya nyata untuk memvalidasi ketahanan model terhadap variasi kondisi jalan,
   cuaca, dan sudut pandang yang lebih beragam.

---

## Checklist Sebelum Sidang

### Dokumen
- [ ] Bab 1: Rumusan masalah & tujuan sudah mencakup video real-time dan perbandingan model
- [ ] Bab 1: Batasan masalah sudah diperbarui (gambar statis → video, evaluasi mAP jadi fokus)
- [ ] Bab 2: Subbab metrik evaluasi sudah ditambahkan
- [ ] Bab 2: Subbab video real-time detection sudah ditambahkan
- [ ] Bab 3: Tabel konfigurasi hyperparameter sudah ada dan dijelaskan per parameter
- [ ] Bab 3: Pembagian data (stratified sampling, alasan 30/kelas) sudah dijelaskan
- [ ] Bab 3: UML sudah diperbarui (use case + activity diagram video real-time)
- [ ] Bab 4: Tabel perbandingan 3 model sudah diisi (sudah ada datanya)
- [ ] Bab 4: Grafik loss training sudah dibuat
- [ ] Bab 4: Confusion matrix sudah dianalisis
- [ ] Bab 4: Pengujian fungsional sudah dilakukan dan dicatat
- [ ] Bab 4: Pengujian kondisi nyata sudah dilakukan dan dicatat
- [ ] Bab 4: Screenshot antarmuka sudah diambil
- [ ] Bab 5: Kesimpulan menjawab semua rumusan masalah
- [ ] Bab 5: Saran sudah ditulis

### Teknis
- [ ] Backend sudah di-restart dan `/dataset/validation` tidak lagi error
- [ ] Sistem video real-time sudah berjalan di browser
- [ ] Semua 3 model sudah bisa dipilih dan diaktifkan dari antarmuka
- [ ] Abstrak sudah diperbarui (mention video real-time, perbandingan model, 18 kelas)
