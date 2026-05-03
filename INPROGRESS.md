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

Catatan UX lanjutan:
- pada `Daftar Model`, kolom `mAP@0.5`, `Precision`, `Recall`, dan `Mean IoU` sebaiknya dihapus dari tabel utama agar tampilan lebih ringkas
- metrik model lebih cocok ditampilkan pada detail model, modal, atau halaman detail terpisah bila nanti diperlukan
- pada `Riwayat Training Run`, kolom `Started At` perlu diformat ke bentuk yang mudah dibaca manusia
  - contoh saat ini: `2026-05-03T07:09:24.720228+00:00`
  - target tampilan: format tanggal dan jam yang lebih natural

### Step 14 — Implement halaman Prediksi
Status: `done`

Target:
- upload gambar
- preview
- tampilkan bbox, label, confidence
- tampilkan model aktif

Output selesai:
- demo end-to-end sudah usable

Catatan UX lanjutan:
- `Preview Hasil Prediksi` dan `Daftar Hasil Deteksi` sebaiknya hanya muncul setelah user menekan prediksi dan API berhasil merespons
- sebelum ada hasil prediksi, jangan tampilkan terlalu banyak komponen agar user tidak bingung
- tombol yang sama-sama me-refresh model aktif pada halaman prediksi perlu dirapikan; cukup sisakan satu tombol refresh saja

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
4. Import model hasil training eksternal ke registry aplikasi
5. Finalisasi workflow cloud GPU untuk training skala besar

Alasannya:
- kecil
- jelas selesaiannya
- risikonya rendah
- hasilnya langsung dipakai banyak fitur berikutnya

## Backlog Setelah Aplikasi Stabil

### Step 16 — Tambahkan fitur import/upload model
Status: `next`

Target:
- upload model hasil training dari luar aplikasi
- registrasikan model ke SQLite registry
- pilih model import sebagai model aktif bila diperlukan
- sediakan juga download model untuk backup atau pemindahan model
- saat import model, tampilkan detail model secara jelas:
  - jumlah kelas
  - daftar nama kelas
  - metrik jika tersedia
  - informasi model dasar dan versi

Output selesai:
- model dari cloud GPU atau training manual bisa dipakai tanpa harus train ulang dari aplikasi lokal
- model yang sudah ada bisa diunduh kembali saat diperlukan
- pengguna bisa memahami isi model yang diimport sebelum dipakai

Kenapa ini penting:
- training final kemungkinan dilakukan di cloud, bukan di laptop lokal

### Step 17 — Tambahkan workflow dataset untuk training cloud
Status: `pending`

Target:
- putuskan strategi distribusi dataset untuk cloud training
- dokumentasikan langkah upload dataset ke environment training
- siapkan checklist sinkronisasi hasil model kembali ke lokal

Output selesai:
- alur cloud training tidak membingungkan saat model final akan dilatih

Kenapa ini penting:
- Docker saat ini belum otomatis membawa dataset lokal ke server cloud

### Step 18 — Tambahkan prediksi dari kamera
Status: `pending`

Target:
- akses kamera dari browser
- ambil foto dari kamera
- kirim hasil capture ke endpoint prediksi yang sudah ada
- tampilkan hasil deteksi seperti mode upload file

Output selesai:
- pengguna bisa melakukan prediksi langsung dari kamera tanpa video real-time

Kenapa ini dipilih:
- paling ringan untuk diimplementasikan
- tidak mengubah arsitektur backend secara besar
- tetap sesuai batasan input gambar statis untuk skripsi

### Step 19 — Tambahkan halaman User Guide
Status: `pending`

Target:
- buat halaman panduan penggunaan aplikasi
- jelaskan alur penggunaan setiap menu
- jelaskan cara training, memilih model aktif, prediksi gambar, dan membaca hasil

Output selesai:
- dosen atau pengguna baru bisa memahami cara memakai aplikasi tanpa penjelasan lisan penuh

Kenapa ini penting:
- membantu demo sidang
- membantu dokumentasi penggunaan sistem

### Step 20 — Tambahkan autentikasi login sederhana
Status: `pending`

Target:
- sediakan login hanya untuk admin tanpa fitur register
- backend menyediakan endpoint login dan profile/session sederhana
- frontend menyimpan token/login state dan melindungi route admin
- logout menghapus token dari browser storage
- akses publik tanpa login tetap tersedia untuk:
  - prediksi
  - user guide
  - penjelasan metode

Catatan implementasi:
- tetap sederhana, tidak perlu manajemen user penuh
- hindari token tanpa tanda tangan
- gunakan token yang ditandatangani backend
- jika memungkinkan gunakan masa berlaku yang wajar walau pendekatan login dibuat sederhana
- jika storage browser dipakai, dokumentasikan bahwa ini kompromi implementasi untuk scope skripsi, bukan desain keamanan tingkat produksi

Output selesai:
- halaman admin terlindungi saat demo, sedangkan halaman publik tetap bisa diakses langsung

Kenapa ini penting:
- konsisten dengan kebutuhan bahwa pengelolaan sistem dilakukan admin
- menjaga fitur prediksi tetap mudah diakses publik

### Step 21 — Tambahkan halaman penjelasan Vision Transformer / YOLOS
Status: `pending`

Target:
- buat halaman penjelasan ringkas namun teknis tentang alur kerja model
- gunakan bahasa yang mudah dipahami untuk dosen non-bidang
- utamakan analogi sederhana sebelum penjelasan teknis
- catat alur sederhana yang harus dijelaskan ke pengguna:
  - gambar statis dikirim dari frontend ke backend
  - backend menyiapkan gambar agar sesuai format model
  - gambar dibagi menjadi bagian-bagian kecil
  - setiap bagian diterjemahkan menjadi data yang bisa dibaca model
  - model melihat hubungan antarbagian gambar
  - model menentukan ada rambu apa dan letaknya di mana
  - hasil dikembalikan sebagai label, confidence, dan bounding box
- jelaskan alur inferensi gambar statis:
  - gambar diterima backend
  - preprocessing oleh image processor
  - resize/normalisasi sesuai kebutuhan model
  - gambar dipecah menjadi patch
  - patch diubah menjadi embedding/token
  - token diproses oleh self-attention transformer
  - model memprediksi kelas dan bounding box
  - hasil dipost-process menjadi label, confidence, dan bbox pada ukuran gambar asli
- jelaskan bahwa YOLOS bukan sekadar klasifikasi gambar penuh, tetapi object detection yang memprediksi lokasi dan kelas objek

Output selesai:
- tersedia menu penjelasan metode yang bisa membantu saat presentasi atau sidang
- isi penjelasan tetap mudah dipahami meskipun pembaca bukan dari bidang computer vision

Kenapa ini penting:
- pengguna perlu memahami logika model walau implementasi memakai library
- membantu menjawab pertanyaan dosen tentang alur Vision Transformer

### Step 22 — Optimasi endpoint dataset dengan cache
Status: `pending`

Target:
- tambahkan cache untuk endpoint dataset summary dan dataset validation
- hindari scan ulang dataset penuh pada setiap request
- jika perlu, tambahkan strategi invalidasi cache saat dataset berubah

Output selesai:
- endpoint dataset terasa lebih cepat dan tidak memakan waktu belasan detik untuk request berulang

Kenapa ini penting:
- scan dataset saat ini terasa lambat pada endpoint summary dan validation
- pengalaman frontend menjadi buruk jika setiap refresh harus menunggu terlalu lama

### Step 23 — Eksekusi training final di cloud GPU
Status: `pending`

Target:
- pilih provider cloud GPU final
- jalankan training semua kelas
- simpan model terbaik
- import model terbaik ke aplikasi lokal

Output selesai:
- tersedia model final untuk evaluasi dan demo skripsi

Kenapa ini diletakkan terakhir:
- biaya cloud GPU lebih efisien jika aplikasi sudah stabil
- model final lebih baik dilatih sekali dengan pipeline yang sudah matang

## Aturan Update File Ini

Saat satu step dimulai:
- ubah status menjadi `in-progress`

Saat satu step selesai:
- ubah status menjadi `done`
- tambahkan tanggal singkat bila perlu

Saat ada perubahan prioritas:
- ubah hanya bagian `next` dan `pending`
