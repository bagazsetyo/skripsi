# Daftar File Training dan Prediksi

Dokumen ini dibuat untuk memudahkan review kode oleh senior atau pihak lain. Fokusnya adalah menunjukkan file mana saja yang berhubungan dengan:
- training model
- evaluasi model
- prediksi gambar
- prediksi video / realtime OpenCV
- konfigurasi model dan dataset

## 1. File Utama untuk Training

### [backend/train.py](/D:/Code/UP-V4/backend/train.py)
Fungsi:
- script training dasar YOLOS
- dipakai untuk menjalankan training manual dari command line

Peran utama:
- membaca argumen training
- memuat dataset training
- membangun model YOLOS
- menjalankan loop training
- menyimpan model hasil training

Catatan:
- ini cocok untuk training manual
- untuk training dari web/backend, alur utamanya lebih banyak memakai `training_service.py`

### [backend/training_core.py](/D:/Code/UP-V4/backend/training_core.py)
Fungsi:
- inti proses training

Peran utama:
- `build_model(...)`
  - membangun model YOLOS sesuai jumlah kelas
- `train_one_epoch(...)`
  - menjalankan 1 epoch training

Catatan:
- ini adalah file inti yang paling relevan kalau ingin meninjau mekanisme belajar model

### [backend/training_service.py](/D:/Code/UP-V4/backend/training_service.py)
Fungsi:
- service training untuk backend/web

Peran utama:
- menerima request training
- membentuk output version model
- memuat dataset train dan test
- membangun optimizer dan scheduler
- menjalankan training per epoch
- menyimpan model
- menjalankan evaluasi
- menyimpan metadata model ke registry SQLite

Catatan:
- ini file paling penting untuk memahami alur training end-to-end di aplikasi

## 2. File Dataset yang Dipakai untuk Training

### [backend/dataset.py](/D:/Code/UP-V4/backend/dataset.py)
Fungsi:
- loader dataset untuk training dan evaluasi

Peran utama:
- membaca folder `train/` dan `test/`
- membaca pasangan `.jpg` dan `.txt`
- membaca anotasi format YOLO
- mengubah anotasi YOLO menjadi target yang bisa dipakai YOLOS
- membangun mapping kelas dari struktur folder

Catatan:
- kalau ada masalah data tidak terbaca, class mismatch, atau label tidak ditemukan, file ini sangat penting untuk dicek

### [backend/dataset_scan.py](/D:/Code/UP-V4/backend/dataset_scan.py)
Fungsi:
- scanner dan validator dataset

Peran utama:
- menghitung statistik dataset
- validasi file gambar dan label
- dipakai untuk endpoint dataset summary dan validation

Catatan:
- ini bukan file training inti, tetapi penting untuk memastikan dataset bersih sebelum training

## 3. File Evaluasi Model

### [backend/evaluation.py](/D:/Code/UP-V4/backend/evaluation.py)
Fungsi:
- evaluasi hasil model pada data test

Peran utama:
- menghitung IoU
- menghitung precision
- menghitung recall
- menghitung mAP@0.5
- menghitung mean IoU
- menghasilkan metrik per kelas

Catatan:
- file ini sangat penting untuk menganalisis kenapa suatu model bagus atau buruk
- jika ada salah klasifikasi, hasil per kelas di file evaluasi bisa membantu diagnosis

## 4. File Prediksi Gambar

### [backend/app/inference.py](/D:/Code/UP-V4/backend/app/inference.py)
Fungsi:
- inference / prediksi gambar

Peran utama:
- load model YOLOS dari folder model
- load processor YOLOS
- melakukan preprocessing gambar
- menjalankan inferensi
- melakukan post-process hasil deteksi
- mengembalikan:
  - label kelas
  - confidence
  - bounding box

Catatan:
- ini file utama untuk menjawab pertanyaan “bagaimana model melakukan prediksi?”

### [backend/app/main.py](/D:/Code/UP-V4/backend/app/main.py)
Fungsi:
- endpoint backend utama FastAPI

Peran utama untuk prediksi:
- endpoint `/predict`
- membaca model aktif
- menerima file gambar
- memanggil `Predictor` dari `inference.py`
- mengembalikan response prediksi ke frontend

Peran lain:
- endpoint training
- endpoint dataset
- endpoint model registry
- endpoint import model
- endpoint video demo backend

Catatan:
- kalau ingin melihat integrasi antara API dan model, file ini sangat penting

## 5. File Prediksi Video / Realtime OpenCV

### [backend/realtime_demo.py](/D:/Code/UP-V4/backend/realtime_demo.py)
Fungsi:
- demo realtime sederhana langsung dari Python + OpenCV

Peran utama:
- membuka kamera atau file video dengan OpenCV
- menampilkan video terus-menerus
- mengambil frame berkala
- mengirim frame ke thread inferensi
- menampilkan bounding box langsung di video
- menampilkan:
  - FPS
  - status `Processing...`
  - confidence
  - label

Arsitektur:
- main loop untuk display video
- worker thread untuk inferensi
- queue `maxsize=1`
- lock untuk hasil prediksi terakhir

Catatan:
- ini file utama jika ingin membahas prediksi video / near real-time dari Python

### [backend/app/video_demo.py](/D:/Code/UP-V4/backend/app/video_demo.py)
Fungsi:
- halaman HTML sederhana untuk video demo dari backend

Peran utama:
- membangun halaman `/video-demo`
- menampilkan kontrol video/kamera di browser
- menampilkan overlay hasil deteksi

Catatan:
- ini lebih ke demo backend page, bukan script OpenCV langsung

## 6. File Konfigurasi Penting

### [backend/config.py](/D:/Code/UP-V4/backend/config.py)
Fungsi:
- pusat konfigurasi utama backend

Peran utama:
- daftar 21 kelas final
- path dataset
- path model
- default hyperparameter
- threshold default
- auth config sederhana

Catatan:
- file ini penting untuk mengecek:
  - nama kelas
  - jumlah kelas
  - path model
  - path dataset

## 7. File Model Registry dan Import Model

### [backend/db.py](/D:/Code/UP-V4/backend/db.py)
Fungsi:
- SQLite registry

Peran utama:
- menyimpan metadata model
- menyimpan training runs
- menyimpan dataset cache

Catatan:
- ini penting kalau ingin melihat bagaimana model hasil training disimpan dan dipilih

### [backend/model_registry.py](/D:/Code/UP-V4/backend/model_registry.py)
Fungsi:
- helper registry model aktif

Peran utama:
- memastikan model default terdaftar
- mengatur model aktif
- membaca path model aktif

### [backend/model_import.py](/D:/Code/UP-V4/backend/model_import.py)
Fungsi:
- import model hasil training eksternal

Peran utama:
- membaca ZIP model dari Colab atau environment lain
- validasi isi model Hugging Face
- membaca metadata seperti:
  - config
  - metrics
  - training summary
- copy model ke `backend/models/`
- registrasikan ke SQLite

Catatan:
- ini penting jika workflow model berasal dari Google Colab

## 8. File Runner Google Colab

### [colab/experiment_runner.py](/D:/Code/UP-V4/colab/experiment_runner.py)
Fungsi:
- runner eksperimen otomatis di Google Colab

Peran utama:
- mount Google Drive
- install dependency
- copy/unzip dataset
- menjalankan training
- menjalankan evaluasi
- menyimpan:
  - model
  - `metrics.json`
  - `training_summary.json`
  - `preset_config.json`

Catatan:
- ini file utama jika ingin memahami workflow training di Colab

### [colab/run_image_500.py](/D:/Code/UP-V4/colab/run_image_500.py)
### [colab/run_image_600.py](/D:/Code/UP-V4/colab/run_image_600.py)
### [colab/run_image_700.py](/D:/Code/UP-V4/colab/run_image_700.py)
Fungsi:
- preset eksperimen untuk perbandingan image size

Peran utama:
- menjalankan preset `500`
- menjalankan preset `600`
- menjalankan preset `700`

Catatan:
- file-file ini penting untuk Bab 4 karena langsung mewakili konfigurasi eksperimen yang dibandingkan

## 9. Jika Senior Ingin Review Cepat

Kalau senior hanya ingin melihat file paling penting, kirim urutan ini:

1. [backend/training_service.py](/D:/Code/UP-V4/backend/training_service.py)
2. [backend/training_core.py](/D:/Code/UP-V4/backend/training_core.py)
3. [backend/dataset.py](/D:/Code/UP-V4/backend/dataset.py)
4. [backend/evaluation.py](/D:/Code/UP-V4/backend/evaluation.py)
5. [backend/app/inference.py](/D:/Code/UP-V4/backend/app/inference.py)
6. [backend/realtime_demo.py](/D:/Code/UP-V4/backend/realtime_demo.py)
7. [backend/config.py](/D:/Code/UP-V4/backend/config.py)

## 10. Ringkasan Singkat

- **Training utama**: `backend/training_service.py`, `backend/training_core.py`, `backend/dataset.py`
- **Evaluasi model**: `backend/evaluation.py`
- **Prediksi gambar**: `backend/app/inference.py`, `backend/app/main.py`
- **Prediksi video OpenCV**: `backend/realtime_demo.py`
- **Training Colab**: `colab/experiment_runner.py`, `colab/run_image_500.py`, `colab/run_image_600.py`, `colab/run_image_700.py`
- **Import model dari Colab**: `backend/model_import.py`
