# TODO Skripsi

Dokumen ini adalah daftar kerja terbaru setelah bimbingan. Fokus utama sekarang adalah menyelesaikan aplikasi citra statis, memperkuat eksperimen model, lalu menyiapkan pengujian video / near real-time sebagai pengembangan berikutnya.

## Prioritas 1 — Finalisasi Aplikasi Citra Statis

### 1. Rapikan UI dan UX aplikasi
- rapikan halaman publik dan admin yang masih kurang rapi
- pastikan alur prediksi, training, dataset, dan dashboard nyaman dipakai
- samakan istilah di seluruh aplikasi

### 2. Uji manual end-to-end
- uji login admin
- uji dataset summary, validation, dan refresh
- uji training model dari web
- uji aktivasi model
- uji prediksi upload gambar
- uji prediksi dari kamera snapshot

### 3. Rapikan dokumentasi penggunaan
- finalkan halaman `User Guide`
- finalkan halaman `Cara Kerja YOLOS`
- ganti placeholder dengan screenshot final bila sudah siap

### 4. Siapkan bukti implementasi
- screenshot Dashboard
- screenshot Dataset
- screenshot Training & Model
- screenshot Prediksi
- screenshot hasil deteksi bounding box

## Prioritas 2 — Perkuat Penelitian dan Eksperimen Model

### 5. Ubah strategi pembagian data menjadi 80:20
- evaluasi dataset train/test saat ini
- jika mengikuti arahan dosen, gabungkan lalu split ulang menjadi 80:20
- usahakan pembagian seimbang per kelas
- dokumentasikan proses split agar jelas di Bab 3

### 6. Siapkan beberapa konfigurasi eksperimen
- buat beberapa kombinasi hyperparameter
- fokus pembanding awal:
  - image size
  - learning rate
  - batch size
  - epoch
- rekomendasi awal image size:
  - `384`
  - `512`
  - `640`

### 7. Jalankan eksperimen model
- train beberapa konfigurasi yang realistis
- bandingkan hasilnya
- pilih model terbaik untuk demo aplikasi

### 8. Tampilkan hasil pengujian model
- tampilkan loss akhir
- tampilkan precision
- tampilkan recall
- tampilkan mAP@0.5
- tampilkan mean IoU
- siapkan tabel perbandingan model untuk Bab 4

## Prioritas 3 — Workflow Model Eksternal

### 9. Tambahkan import/upload model
- upload model hasil training dari luar aplikasi
- registrasikan model ke SQLite
- tampilkan metadata model:
  - jumlah kelas
  - nama kelas
  - metrik jika tersedia
  - informasi model dasar / versi

### 10. Tambahkan download/export model
- download model untuk backup
- download model untuk dipindahkan dari cloud ke lokal

### 11. Siapkan workflow training di cloud GPU
- pilih provider yang akan dipakai
- siapkan langkah upload dataset
- siapkan langkah training model di cloud
- siapkan langkah membawa model kembali ke aplikasi lokal

## Prioritas 4 — Pengujian Video / Near Real-Time

### 12. Opsi utama: kamera/video di frontend, inferensi di backend
- frontend membuka kamera atau video
- frontend mengambil frame berkala
- interval awal:
  - `1 detik`
  - lalu coba `0.5 detik` jika memungkinkan
- frame dikirim ke backend
- backend menjalankan inferensi YOLOS
- frontend menampilkan hasil deteksi di atas video/frame

Catatan:
- gunakan satu request aktif pada satu waktu
- jangan kirim frame baru sebelum hasil sebelumnya kembali
- targetnya adalah **near real-time**, bukan hard real-time

### 13. Opsi kedua: page realtime terpisah di backend
- backend menyediakan page khusus realtime
- inferensi dan alur video lebih banyak ditangani backend

Catatan:
- ini hanya alternatif kedua
- dipilih bila opsi utama terlalu sulit atau tidak stabil

## Prioritas 5 — Penulisan Skripsi

### 14. Perkuat Bab 3
- tambahkan konfigurasi eksperimen lebih banyak
- tambahkan skenario pengujian
- tambahkan alasan pembagian data
- tambahkan rancangan pengujian model

### 15. Perkuat Bab 4
- tampilkan pengujian aplikasi
- tampilkan pengujian model
- tampilkan perbandingan beberapa konfigurasi
- analisis model terbaik

## Keputusan Penting Saat Ini

- fokus utama tetap **gambar statis**
- video / realtime dikerjakan setelah citra statis stabil
- model tetap memakai **YOLOS / Vision Transformer**
- jangan ganti metode kecuali ada instruksi eksplisit dari dosen pembimbing
- training final diarahkan ke **cloud GPU**
- fitur import/export model sekarang dianggap penting

## Definisi Selesai Minimum

Skripsi dianggap cukup aman jika:
- aplikasi citra statis final dan stabil
- ada beberapa eksperimen konfigurasi model
- ada model terbaik yang dipilih
- hasil pengujian model ditampilkan dengan jelas
- model cloud bisa diimport ke aplikasi
- ada bukti implementasi dan pengujian untuk Bab 4
