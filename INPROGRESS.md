# INPROGRESS

Dokumen ini dipakai untuk tracking urutan kerja aktual setelah hasil bimbingan terbaru. `TODO.md` menjadi daftar kerja utama, sedangkan file ini fokus ke urutan eksekusi yang paling realistis untuk dikerjakan sekarang.

## Prinsip Pengerjaan

- Selesaikan dulu aplikasi citra statis
- Dahulukan task kecil yang langsung memperkuat demo dan skripsi
- Eksperimen model harus mulai dinaikkan prioritasnya
- Video / near real-time dikerjakan setelah alur citra statis stabil
- Cloud GPU dan import/export model mengikuti kebutuhan eksperimen final

## Status Pekerjaan yang Sudah Selesai

### Fondasi Backend
Status: `done`

Output selesai:
- konfigurasi backend sinkron ke 21 kelas
- class mapping terpusat
- dataset scanner dan validator tersedia
- endpoint dataset tersedia
- training service dasar tersedia
- model registry SQLite tersedia
- prediksi membaca model aktif
- evaluasi model dasar tersedia

### Fondasi Frontend
Status: `done`

Output selesai:
- frontend React sudah ada
- struktur frontend sudah dirapikan
- dashboard, dataset, training, dan prediksi sudah tersedia
- user guide dan halaman penjelasan YOLOS sudah tersedia

### Infrastruktur dan Optimasi Dasar
Status: `done`

Output selesai:
- docker development backend dan frontend sudah siap
- CORS sudah diaktifkan
- dataset summary dan validation sudah memakai snapshot SQLite
- refresh dataset sudah jalan di background

### Fitur Akses dan Prediksi
Status: `done`

Output selesai:
- login admin sederhana sudah tersedia
- halaman publik tetap bisa diakses tanpa login
- prediksi upload gambar sudah stabil
- prediksi kamera snapshot sudah tersedia

## Urutan Kerja Baru

### Step 1 — Finalkan aplikasi citra statis
Status: `next`

Target:
- rapikan UI/UX kecil yang masih tersisa
- uji manual seluruh alur utama
- cek konsistensi istilah dan tampilan
- siapkan screenshot implementasi final

Output selesai:
- aplikasi siap dipakai demo
- halaman utama stabil untuk dokumentasi Bab 4

### Step 2 — Finalkan dokumentasi aplikasi
Status: `pending`

Target:
- rapikan isi `User Guide`
- rapikan isi halaman `Cara Kerja YOLOS`
- ganti placeholder dengan screenshot final bila sudah siap

Output selesai:
- dokumentasi penggunaan aplikasi siap dipakai saat sidang

### Step 3 — Ubah strategi dataset menjadi 80:20
Status: `pending`

Target:
- evaluasi dataset train/test yang ada sekarang
- jika disetujui, gabungkan lalu split ulang 80:20
- dokumentasikan proses pembagian data

Output selesai:
- dataset sesuai arahan bimbingan
- dasar pengujian model lebih kuat untuk skripsi

### Step 4 — Siapkan skenario eksperimen model
Status: `pending`

Target:
- tetapkan beberapa konfigurasi training yang akan dibandingkan
- fokus awal:
  - image size
  - learning rate
  - batch size
  - epoch

Output selesai:
- ada daftar eksperimen yang jelas sebelum training final dijalankan

### Step 5 — Jalankan eksperimen model
Status: `pending`

Target:
- training beberapa konfigurasi yang realistis
- bandingkan metrik tiap model
- pilih model terbaik

Output selesai:
- tersedia hasil eksperimen yang bisa masuk Bab 4

### Step 6 — Tambahkan import/upload model
Status: `pending`

Target:
- upload model hasil training dari luar aplikasi
- simpan ke registry
- tampilkan metadata model:
  - jumlah kelas
  - nama kelas
  - metrik jika tersedia
  - informasi model dasar / versi

Output selesai:
- model hasil cloud training bisa dipakai di aplikasi lokal

### Step 7 — Tambahkan download/export model
Status: `pending`

Target:
- download model untuk backup
- download model untuk pemindahan

Output selesai:
- model mudah dipindahkan antara cloud dan lokal

### Step 8 — Siapkan workflow training cloud GPU
Status: `pending`

Target:
- pilih provider cloud GPU final
- siapkan alur upload dataset
- siapkan alur training
- siapkan alur import model kembali ke aplikasi

Output selesai:
- training final di cloud lebih siap dijalankan

### Step 9 — Tambahkan pengujian video / near real-time
Status: `pending`

Target:
- opsi utama:
  - frontend membuka kamera/video
  - frontend mengambil frame berkala
  - backend menjalankan inferensi
- mulai dari interval:
  - `1 detik`
  - lalu `0.5 detik` bila memungkinkan
- gunakan satu request aktif pada satu waktu

Output selesai:
- tersedia mode near real-time yang masih konsisten dengan arsitektur sekarang

Catatan:
- page realtime terpisah di backend hanya menjadi opsi kedua
- jangan dikerjakan lebih dulu kecuali opsi utama gagal atau terlalu berat

### Step 10 — Perkuat Bab 3 dan Bab 4
Status: `pending`

Target:
- tambahkan konfigurasi eksperimen ke Bab 3
- tambahkan skenario pengujian ke Bab 3
- tambahkan hasil pengujian aplikasi dan model ke Bab 4
- tambahkan analisis model terbaik

Output selesai:
- dokumen skripsi selaras dengan implementasi dan hasil eksperimen

## Fokus Kerja Saat Ini

Kerjakan dulu:
1. finalisasi aplikasi citra statis
2. finalisasi dokumentasi aplikasi
3. keputusan dan implementasi split dataset 80:20
4. perencanaan eksperimen model

Tunda dulu:
1. cloud GPU skala penuh
2. export/import model bila belum dibutuhkan langsung
3. video / near real-time sebelum mode citra statis benar-benar stabil

## Aturan Update File Ini

Saat satu step dimulai:
- ubah status menjadi `in-progress`

Saat satu step selesai:
- ubah status menjadi `done`

Saat prioritas berubah:
- cukup ubah urutan step dan bagian `Fokus Kerja Saat Ini`
