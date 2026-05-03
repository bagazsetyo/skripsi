# INPROGRESS

Dokumen ini dipakai untuk tracking urutan kerja aktual. `TODO.md` tetap menjadi master list, sedangkan file ini fokus ke langkah kecil yang realistis untuk dikerjakan berurutan.

## Prinsip Pengerjaan

- Kerjakan fondasi backend dulu sebelum frontend penuh
- Setiap task harus cukup kecil untuk selesai dalam 1 sesi kerja
- Jangan mulai halaman frontend yang bergantung pada API yang belum stabil
- Utamakan fitur yang membuka jalan untuk fitur berikutnya

## Rekomendasi Urutan Kerja

### Step 1 — Rapikan konfigurasi dasar backend
Status: `done`

Target:
- `backend/config.py` sinkron ke 21 kelas final
- path dataset dan model dirapikan
- `docker-compose.yml` diperbaiki

Output selesai:
- backend membaca kelas yang benar
- docker tidak salah mount model path

Kenapa ini dulu:
- hampir semua fitur lain bergantung pada konfigurasi kelas dan path yang benar

### Step 2 — Buat sumber data kelas yang tunggal
Status: `done`

Target:
- satu sumber mapping untuk:
  - class id
  - nama label
  - nama folder

Output selesai:
- training, inference, dataset page, dan model registry tidak memakai daftar kelas yang berbeda-beda

Kenapa ini penting:
- sekarang risiko mismatch masih tinggi antara skripsi, dataset, dan kode

### Step 3 — Buat dataset scanner
Status: `done`

Target:
- baca folder `train/` dan `test/`
- hitung jumlah kelas
- hitung jumlah gambar per kelas
- hitung jumlah anotasi per kelas

Output selesai:
- tersedia ringkasan dataset yang bisa dipakai backend dan nanti frontend

Kenapa ini dikerjakan lebih awal:
- halaman Dataset dan validasi training sama-sama butuh data ini

### Step 4 — Tambahkan dataset validator
Status: `done`

Target:
- cek pasangan `.jpg` dan `.txt`
- cek label kosong
- cek class id tidak valid
- cek bbox tidak valid

Output selesai:
- sistem bisa mendeteksi masalah dataset sebelum training dijalankan

Kenapa ini penting:
- mengurangi risiko training gagal karena data kotor

### Step 5 — Buat endpoint dataset
Status: `done`

Target:
- endpoint summary dataset
- endpoint daftar kelas
- endpoint hasil validasi dataset

Output selesai:
- frontend nanti bisa langsung membangun halaman Dataset

### Step 6 — Siapkan training request berbasis subset kelas
Status: `done`

Target:
- desain request training:
  - nama model
  - pilih semua kelas atau subset kelas
  - hyperparameter dasar

Output selesai:
- kontrak API training sudah jelas meskipun training service belum penuh

Kenapa ini sebelum frontend:
- form training di frontend bergantung pada struktur request ini

### Step 7 — Buat model registry dengan SQLite
Status: `done`

Target:
- tabel model
- tabel training run
- field model aktif

Output selesai:
- sistem bisa menyimpan banyak model dan memilih model aktif

Kenapa ini sangat penting:
- ini inti kebutuhan skripsi Anda, bukan hanya sekali train lalu inferensi

### Step 8 — Hubungkan inference ke model aktif
Status: `done`

Target:
- endpoint prediksi membaca model aktif dari registry
- response mengembalikan info model aktif

Output selesai:
- prediksi tidak lagi hardcoded ke satu folder model

### Step 9 — Refactor training script jadi service
Status: `done`

Target:
- `train.py` tidak hanya CLI
- training bisa dipanggil dari backend
- simpan metadata hasil training

Output selesai:
- backend siap menerima trigger training dari web

### Step 10 — Tambahkan hasil evaluasi model
Status: `done`

Target:
- evaluasi pada test set
- simpan precision, recall, IoU, mAP

Output selesai:
- ada data kuantitatif untuk Bab 4 dan detail model

### Step 11 — Baru mulai scaffold frontend
Status: `done`

Target:
- buat folder `frontend`
- setup React
- setup React Router
- setup React Query
- setup Axios
- setup Ant Design

Output selesai:
- project frontend siap dikembangkan

Kenapa belum dikerjakan sekarang:
- lebih efisien bila kontrak API inti sudah terbentuk dulu

### Step 12 — Implement halaman Dataset dulu
Status: `done`

Target:
- tampilkan daftar kelas
- tampilkan statistik dataset
- tampilkan hasil validasi

Output selesai:
- frontend pertama jadi tanpa tergantung training kompleks

Kenapa ini halaman pertama:
- paling ringan, paling aman, dan langsung memakai endpoint yang stabil

### Step 13 — Implement halaman Training & Model
Status: `done`

Target:
- form training
- multi-select kelas
- daftar model
- set active model

Output selesai:
- alur inti skripsi mulai terlihat

### Step 14 — Implement halaman Prediksi
Status: `done`

Target:
- upload gambar
- preview
- tampilkan bbox, label, confidence
- tampilkan model aktif

Output selesai:
- demo end-to-end sudah usable

### Step 15 — Implement Dashboard
Status: `done`

Target:
- ringkasan model aktif
- jumlah data
- jumlah model
- training terakhir
- metrik model aktif

Output selesai:
- UI lengkap untuk screenshot implementasi skripsi

## Yang Sebaiknya Dikerjakan Sekarang

Kalau ingin paling aman dan paling efisien, mulai dari tiga task ini dulu:

1. Polishing UI dan integrasi end-to-end
2. Uji manual seluruh alur aplikasi
3. Dokumentasi screenshot untuk skripsi

Alasannya:
- kecil
- jelas selesaiannya
- risikonya rendah
- hasilnya langsung dipakai banyak fitur berikutnya

## Aturan Update File Ini

Saat satu step dimulai:
- ubah status menjadi `in-progress`

Saat satu step selesai:
- ubah status menjadi `done`
- tambahkan tanggal singkat bila perlu

Saat ada perubahan prioritas:
- ubah hanya bagian `next` dan `pending`
