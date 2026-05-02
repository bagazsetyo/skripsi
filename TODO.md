# TODO Aplikasi Skripsi

Dokumen ini berisi breakdown task untuk mendukung pembuatan aplikasi skripsi berjudul **Deteksi dan Klasifikasi Rambu Lalu Lintas Indonesia Menggunakan Vision Transformer**. Fokusnya adalah menutup gap antara rancangan pada `skirpsi.md`, mockup pada `text.txt`, dan implementasi backend yang saat ini sudah berjalan untuk testing.

## 1. Ringkasan Kondisi Saat Ini

### Sudah ada
- Script training YOLOS dasar di `backend/train.py`
- Loader dataset YOLO dasar di `backend/dataset.py`
- API FastAPI untuk health check dan prediksi gambar di `backend/app/main.py`
- Kode inference YOLOS di `backend/app/inference.py`
- Model hasil training tersimpan di `backend/models/yolos`
- Dockerfile backend dan `docker-compose.yml`

### Belum ada / belum lengkap
- Belum ada frontend React di repo
- Belum ada fitur training via web
- Belum ada manajemen model berbasis database
- Belum ada SQLite untuk metadata model / riwayat training
- Belum ada dataset explorer / dataset validation endpoint
- Belum ada dashboard
- Belum ada endpoint evaluasi model
- Belum ada penyimpanan history training yang rapi
- Belum ada visualisasi hasil prediksi yang sesuai kebutuhan skripsi

### Catatan penting hasil review
- File skripsi bernama `skirpsi.md`, bukan `skripsi.md`
- `docker-compose.yml` pada service `backend` me-mount volume ke `/app/backend/modelsz`; ini terlihat typo dan berpotensi membuat model API tidak terbaca
- `backend/config.py` baru berisi 2 kelas, padahal dataset dan Bab 3 menuliskan 21 kelas
- Mockup `text.txt` masih bersifat wireframe; UI final perlu dibuat lebih matang dari mockup tersebut
- Di `text.txt` tertulis 43 kelas, tetapi dataset aktual di `data/traffic_sign` berisi 21 folder kelas pada `train` dan 21 folder kelas pada `test`

## 2. Task Prioritas Utama

### A. Penyelarasan kebutuhan skripsi dan implementasi
- Finalkan ruang lingkup aplikasi:
  - apakah aplikasi hanya untuk demo lokal
  - apakah training dijalankan sinkron dari web atau dipicu sebagai background job
- Semua 21 kelas pada dataset dipakai sebagai ruang lingkup final
- Sistem harus mendukung training dengan dua mode:
  - semua kelas
  - subset kelas tertentu, misalnya kelas 1, 2, dan 3 saja
- Finalkan daftar fitur minimum untuk Bab Implementasi:
  - dashboard
  - dataset
  - training & model
  - prediksi
- Finalkan istilah yang konsisten:
  - YOLOS / Vision Transformer
  - deteksi dan klasifikasi
  - model aktif
  - riwayat training

### B. Perapihan fondasi backend
- Rapikan konfigurasi global:
  - path dataset
  - path model
  - environment variable
  - score threshold default
- Sinkronkan `CLASS_NAMES` dengan dataset aktual 21 kelas
- Buat validasi startup:
  - cek model directory
  - cek dataset directory
  - cek jumlah kelas
- Perbaiki konfigurasi Docker dan docker-compose
- Tambahkan struktur folder yang jelas untuk:
  - model registry
  - artifacts training
  - logs
  - temporary upload

## 3. Breakdown Task Backend

### 3.1 Dataset Management
- Buat service untuk scan dataset
- Buat endpoint untuk membaca struktur dataset
- Hitung statistik dataset:
  - jumlah kelas
  - jumlah gambar train
  - jumlah gambar test
  - jumlah anotasi per kelas
- Buat validasi dataset:
  - pasangan `.jpg` dan `.txt`
  - file rusak
  - label kosong
  - class id di luar mapping
  - bbox tidak valid
- Tambahkan dukungan filtering dataset berdasarkan kelas terpilih
- Pastikan backend bisa membentuk subset training dari daftar kelas yang dipilih user
- Buat output ringkasan dataset untuk kebutuhan halaman Dataset
- Siapkan data tabel untuk kebutuhan Bab 3 dan Bab 4

### 3.2 Class Mapping dan Konfigurasi Model
- Pusatkan mapping `class_id -> label -> nama folder`
- Pastikan mapping cocok dengan `maping-kode.txt` dan isi dataset
- Siapkan daftar 21 kelas final sebagai sumber tunggal untuk:
  - dataset page
  - form training
  - inference response
  - evaluasi
- Buat konfigurasi model yang bisa diganti:
  - nama model YOLOS
  - image size
  - batch size
  - epoch
  - learning rate
  - optimizer
  - scheduler
- Tambahkan file konfigurasi eksperimen agar training tidak tergantung hardcode

### 3.3 Training Service
- Refactor `train.py` agar bisa dipanggil dari API/service internal
- Pisahkan modul:
  - data loading
  - training loop
  - evaluasi
  - save artifact
  - logging
- Tambahkan pencatatan progress training:
  - status
  - epoch berjalan
  - loss per epoch
  - waktu mulai dan selesai
- Tambahkan input request training:
  - nama eksperimen / nama model
  - daftar kelas terpilih
  - hyperparameter
- Simpan hasil training per versi model
- Simpan metadata training:
  - parameter training
  - jumlah kelas
  - daftar kelas yang dipakai
  - dataset yang dipakai
  - hasil evaluasi
- Tentukan mekanisme training:
  - blocking sederhana
  - thread/background task
  - queue sederhana

### 3.4 Model Registry
- Buat SQLite untuk menyimpan metadata model
- Desain tabel minimum:
  - `models`
  - `training_runs`
  - opsional `dataset_snapshots`
- Simpan field penting:
  - id
  - version
  - model_name
  - path
  - created_at
  - status
  - active flag
  - metrics
- Simpan juga:
  - jumlah kelas model
  - daftar kelas yang dipakai saat training
  - konfigurasi hyperparameter
- Buat endpoint:
  - list model
  - detail model
  - set active model
  - hapus/nonaktifkan model bila diperlukan
- Pastikan API prediksi selalu membaca model aktif

### 3.5 Inference dan Prediksi
- Rapikan endpoint `/predict`
- Tambahkan validasi file upload
- Tambahkan opsi threshold confidence dari request
- Tambahkan informasi model aktif pada response
- Tambahkan format response yang ramah frontend:
  - ukuran gambar
  - daftar bounding box
  - label
  - confidence
  - warna/kelas bila perlu
- Pertimbangkan endpoint tambahan:
  - preview hasil prediksi dengan gambar beranotasi
  - batch predict untuk beberapa gambar

### 3.6 Evaluasi Model
- Buat pipeline evaluasi pada data test
- Hitung metrik:
  - IoU
  - precision
  - recall
  - mAP
- Simpan hasil evaluasi per model
- Buat endpoint untuk melihat hasil evaluasi
- Siapkan output yang bisa langsung dipakai pada Bab 4:
  - tabel metrik keseluruhan
  - tabel per kelas
  - confusion insight sederhana bila memungkinkan

### 3.7 API Dokumentasi dan Kualitas
- Lengkapi schema request/response
- Rapikan error handling
- Tambahkan logging backend
- Tambahkan dokumentasi endpoint
- Tambahkan contoh payload untuk pengujian manual

## 4. Breakdown Task Frontend

Karena frontend belum ada di repo, task frontend perlu dianggap sebagai implementasi baru.

### 4.1 Fondasi Frontend
- Inisialisasi project React di folder `frontend`
- Gunakan stack:
  - React
  - React Router
  - React Query
  - Axios
- Pilih UI library yang ringan dan lengkap
- Rekomendasi: **Ant Design**
  - alasan:
    - komponen data-heavy lengkap untuk dashboard admin
    - tabel, form, upload, badge, tabs, drawer, progress, result sudah siap
    - cocok untuk halaman training, dataset, dan model registry
    - lebih cepat dirakit untuk kebutuhan skripsi
- Buat struktur halaman:
  - Dashboard
  - Training & Model
  - Dataset
  - Prediksi

### 4.2 Arah Desain UI
- Jadikan `text.txt` sebagai acuan struktur, bukan tampilan final
- Tingkatkan kualitas visual:
  - hierarki tipografi lebih kuat
  - warna lebih hidup tetapi tetap akademik/profesional
  - kartu statistik yang lebih jelas
  - tabel model yang lebih rapi
  - status training lebih informatif
  - halaman prediksi dengan area preview yang dominan
- Pastikan layout nyaman di desktop dan tetap usable di laptop kecil
- Buat desain yang cukup presentable untuk screenshot skripsi

### 4.3 Halaman Dashboard
- Tampilkan:
  - model aktif
  - jumlah kelas
  - jumlah data train/test
  - jumlah model tersimpan
  - training terakhir
  - ringkasan metrik model aktif
- Tambahkan status badge untuk model aktif dan kondisi sistem

### 4.4 Halaman Dataset
- Tampilkan struktur dataset
- Tampilkan daftar kelas
- Tampilkan jumlah data per kelas
- Tampilkan hasil validasi dataset
- Tambahkan aksi scan / refresh dataset

### 4.5 Halaman Training & Model
- Form konfigurasi training
- Multi-select kelas untuk memilih subset data training
- Opsi cepat:
  - gunakan semua kelas
  - pilih kelas tertentu
- Tombol mulai training
- Status training berjalan
- Riwayat model
- Aksi set active model
- Detail model:
  - parameter training
  - daftar kelas yang dipakai
  - waktu training
  - metrik evaluasi

### 4.6 Halaman Prediksi
- Upload gambar
- Preview gambar
- Tampilkan hasil bounding box
- Tampilkan daftar objek terdeteksi
- Tampilkan confidence score
- Tampilkan model aktif yang digunakan
- Tambahkan empty state, loading state, dan error state

## 5. Integrasi Sistem

### Integrasi frontend-backend
- Definisikan kontrak API yang stabil
- Buat service layer / API client di frontend
- Standarkan format response backend
- Tangani loading, error, retry, dan timeout

### Integrasi model dan database
- Saat training selesai:
  - model disimpan
  - metadata masuk database
  - model bisa dipilih sebagai aktif
- Saat prediksi:
  - backend membaca model aktif
  - frontend menampilkan informasi model aktif

### Integrasi Docker
- Pastikan backend, frontend, dan database lokal bisa jalan konsisten
- Rapikan volume mount
- Siapkan perintah run yang mudah direplikasi untuk demo

## 6. Testing dan Validasi

### Backend
- Unit test parsing dataset
- Unit test mapping kelas
- Test endpoint health
- Test endpoint predict
- Test endpoint model registry
- Test endpoint dataset summary

### Frontend
- Test render halaman utama
- Test form training
- Test upload prediksi
- Test state loading/error

### End-to-end
- Skenario:
  - scan dataset
  - jalankan training
  - model tersimpan
  - aktifkan model
  - upload gambar
  - hasil deteksi tampil

## 7. Kebutuhan Khusus untuk Penulisan Skripsi

### Bukti implementasi
- Screenshot Dashboard
- Screenshot halaman Dataset
- Screenshot halaman Training & Model
- Screenshot halaman Prediksi
- Screenshot hasil deteksi dengan bounding box
- Screenshot Swagger/OpenAPI bila diperlukan

### Data untuk Bab Implementasi dan Pengujian
- Tabel fitur yang diimplementasikan
- Tabel konfigurasi training
- Tabel daftar kelas final
- Tabel hasil evaluasi model
- Tabel hasil uji fungsional sistem

### Artefak pendukung
- Diagram arsitektur final sesuai implementasi
- Penyesuaian UML bila implementasi berubah dari rancangan awal
- Ringkasan flow training aktual
- Ringkasan flow prediksi aktual

## 8. Urutan Pengerjaan yang Disarankan

### Tahap 1 — Penyelarasan dan fondasi
- Sinkronkan jumlah kelas dan mapping
- Rapikan config
- Perbaiki docker-compose
- Tentukan struktur model registry

### Tahap 2 — Backend inti
- Dataset scan + validation
- Model registry + SQLite
- Training service
- Evaluasi model
- Endpoint pendukung frontend

### Tahap 3 — Frontend inti
- Setup `frontend` dengan React, React Router, React Query, Axios, dan Ant Design
- Implement Dashboard
- Implement Dataset page
- Implement Training & Model page
- Implement Prediksi page

### Tahap 4 — Integrasi dan polishing
- Sambungkan semua endpoint
- Rapikan state loading/error
- Tingkatkan kualitas visual dari mockup
- Siapkan screenshot untuk skripsi

### Tahap 5 — Pengujian dan dokumentasi
- Uji fungsional end-to-end
- Catat hasil evaluasi model
- Lengkapi isi Bab Implementasi dan Pengujian

## 9. Keputusan Scope yang Sudah Dikonfirmasi

- Versi final aplikasi menargetkan **21 kelas** sesuai dataset di repo saat ini
- Sistem harus mendukung training semua kelas atau subset kelas terpilih
- Setiap hasil training menjadi model baru yang tersimpan sebagai versi terpisah
- Sistem harus mendukung pemilihan model aktif untuk prediksi
- Frontend akan dibuat dalam folder `frontend`
- Stack frontend: React, React Router, React Query, Axios
- UI library yang direkomendasikan: Ant Design

## 10. Open Questions yang Masih Tersisa

- Apakah training dari web cukup men-trigger proses dan melihat status periodik, atau harus streaming progress per epoch secara real-time?
- Apakah evaluasi model akan ditampilkan di UI, atau cukup disimpan untuk kebutuhan skripsi?
- Apakah SQLite memang wajib dipakai pada implementasi final, atau masih opsional?

## 11. Definisi Selesai Minimum

Aplikasi dapat dianggap cukup untuk kebutuhan skripsi bila:
- pengguna bisa melihat ringkasan dataset dan model
- admin bisa memulai training dari web dengan semua kelas atau subset kelas
- hasil training tersimpan sebagai versi model
- admin bisa memilih model aktif
- pengguna bisa upload gambar dan melihat hasil deteksi
- tersedia metrik evaluasi model untuk bahan analisis skripsi
- UI cukup rapi untuk dijadikan screenshot implementasi
