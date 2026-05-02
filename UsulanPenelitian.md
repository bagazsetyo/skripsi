# Usulan Penelitian

## Judul
Deteksi dan Klasifikasi Rambu Lalu Lintas Indonesia menggunakan Vision Transformer

---

## BAB 1 — PENDAHULUAN

### Latar Belakang
Rambu lalu lintas berperan penting sebagai media komunikasi visual antara pengelola jalan dan pengguna jalan untuk menjaga keselamatan serta ketertiban berkendara. Ketepatan pengenalan rambu sangat memengaruhi keputusan pengemudi, terutama pada kondisi jalan yang padat dan beragam.

Seiring berkembangnya sistem bantuan pengemudi dan analitik transportasi, dibutuhkan sistem otomatis yang mampu melakukan deteksi (lokasi) dan klasifikasi (jenis) rambu pada citra jalan. Sistem ini dapat digunakan untuk pemantauan, evaluasi infrastruktur, maupun sebagai komponen awal pada sistem pengemudian cerdas.

Namun, citra jalan memiliki tantangan yang kompleks. Rambu sering berukuran kecil, mengalami perubahan pencahayaan, blur, sudut kamera yang bervariasi, tertutup sebagian (occlusion), serta berada pada latar belakang yang ramai. Tantangan ini menyebabkan performa metode konvensional berbasis fitur buatan atau pendekatan sebelumnya kurang stabil, terutama pada objek kecil.

Untuk mengatasi keterbatasan tersebut, penelitian ini memilih pendekatan Vision Transformer, khususnya YOLOS, yang memodelkan citra sebagai urutan patch dan menangkap konteks global secara lebih kuat. Pendekatan ini diharapkan lebih adaptif terhadap variasi kondisi visual di jalan.

Dataset yang digunakan berasal dari Kaggle dan berisi gambar rambu lalu lintas Indonesia dengan anotasi bounding box. Dataset ini dipilih karena relevan dengan konteks lokal serta memiliki struktur train/test yang jelas, sehingga cocok untuk penelitian deteksi objek dan dapat dikembangkan dengan penambahan kelas di masa depan.

### Rumusan Masalah
1. Bagaimana menerapkan Vision Transformer (YOLOS) untuk mendeteksi dan mengklasifikasi rambu lalu lintas Indonesia pada citra jalan?
2. Bagaimana performa model YOLOS pada dataset rambu Indonesia berdasarkan metrik evaluasi deteksi objek (IoU, precision, recall, mAP)?
3. Bagaimana merancang dan membangun sistem berbasis web (FastAPI–React) untuk proses training, manajemen model, dan prediksi?

### Tujuan
1. Mengimplementasikan model deteksi rambu menggunakan YOLOS (Vision Transformer) pada dataset rambu lalu lintas Indonesia.
2. Melakukan pelatihan, validasi, dan pengujian model serta menghitung metrik evaluasi (IoU, precision, recall, mAP).
3. Membangun prototipe sistem web berbasis FastAPI–React untuk upload gambar, prediksi, serta menampilkan hasil deteksi.

### Batasan Masalah
- Data yang digunakan hanya dataset rambu lalu lintas Indonesia dari Kaggle.
- Input berupa gambar statis, bukan video real-time.
- Output hanya bounding box, label kelas, dan confidence.
- Kelas rambu mengikuti kelas yang tersedia pada dataset dan dapat ditambah di masa depan.
- Tidak membahas tracking kendaraan, OCR teks rambu, maupun pengambilan keputusan mengemudi.
- Optimasi real-time/edge deployment tidak menjadi fokus utama.

### Metodologi
1. Studi literatur terkait deteksi rambu dan transformer untuk object detection.
2. Pengumpulan dataset rambu Indonesia dan analisis struktur data serta label.
3. Preprocessing data (resize, normalisasi, augmentasi opsional) dan pembagian data train/val/test.
4. Implementasi model YOLOS (konfigurasi model, jumlah kelas, parameter training).
5. Training dan tuning hyperparameter (epochs, learning rate, batch size, optimizer, scheduler).
6. Evaluasi model menggunakan IoU, precision, recall, mAP serta analisis hasil prediksi.
7. Implementasi sistem web FastAPI–React untuk demo deteksi dan klasifikasi rambu.
8. Pengujian fungsional sistem dan dokumentasi hasil.

---

## BAB 2 — LANDASAN TEORI DAN PENELITIAN TERKAIT

### 2.1 Konsep Dasar Deteksi Objek
Deteksi objek bertujuan menemukan lokasi dan kelas objek pada suatu citra. Hasil deteksi umumnya berupa bounding box dan label kelas. Proses ini berbeda dari klasifikasi karena tidak hanya mengenali kelas, tetapi juga posisi objek.

### 2.2 Rambu Lalu Lintas dan Karakteristik Objek
Rambu lalu lintas memiliki ciri visual khas seperti bentuk dan warna tertentu, namun sering muncul sebagai objek kecil di citra jalan. Kondisi cuaca dan pencahayaan juga memengaruhi keterbacaan rambu, sehingga deteksi rambu menjadi kasus yang menantang.

### 2.3 Machine Learning dan Deep Learning untuk Computer Vision
Pendekatan berbasis CNN banyak digunakan untuk deteksi objek, namun memiliki keterbatasan pada konteks global. Transformer memperkenalkan mekanisme self-attention yang dapat menangkap hubungan global antar patch citra.

### 2.4 Vision Transformer (ViT)
Vision Transformer memecah citra menjadi patch, mengubahnya menjadi token, lalu memprosesnya menggunakan self-attention dan posisi embedding. Keunggulannya adalah kemampuan menangkap konteks global, sedangkan kekurangannya adalah kebutuhan data besar untuk training dari awal.

### 2.5 YOLOS (You Only Look at One Sequence)
YOLOS merupakan adaptasi Transformer untuk deteksi objek yang memandang deteksi sebagai pemrosesan urutan token. YOLOS menyederhanakan pipeline deteksi dengan memanfaatkan struktur ViT dan menghasilkan prediksi kelas serta bounding box secara end-to-end.

### 2.6 Evaluasi Deteksi Objek
Evaluasi umum untuk deteksi objek meliputi IoU, precision, recall, dan mAP. IoU mengukur kesesuaian antara prediksi dan ground-truth, sedangkan mAP merangkum performa pada berbagai threshold.

### 2.7 Teknologi yang Digunakan
- Python untuk training dan inference.
- FastAPI sebagai backend API.
- React untuk antarmuka web.
- Docker untuk deployment.
- SQLite untuk penyimpanan konfigurasi dan riwayat training.

### 2.8 Penelitian Terkait
Penelitian terkait rambu lalu lintas umumnya menggunakan YOLO, SSD, atau Faster R-CNN sebagai pembanding. Penelitian terbaru juga mulai menggunakan model transformer seperti DETR/YOLOS untuk deteksi. Gap penelitian ini adalah fokus pada rambu lalu lintas Indonesia, penggunaan Vision Transformer, dan integrasi sistem web end-to-end.

---

## BAB 3 — PERANCANGAN

### 3.1 Metodologi Penelitian
Tahapan penelitian meliputi studi literatur, pengumpulan dan analisis dataset, preprocessing dan augmentasi, implementasi YOLOS, training dan evaluasi metrik deteksi, integrasi sistem FastAPI–React, serta pengujian fungsional.

### 3.2 Data-data Penelitian
Dataset bersumber dari Kaggle dengan struktur folder `data/traffic_sign/train` dan `data/traffic_sign/test`. Setiap kelas berisi gambar dan file anotasi format YOLO. Contoh anotasi:

```
0 0.247748 0.822957 0.144144 0.206226
```

Jumlah data per kelas akan disajikan dalam tabel pada dokumen akhir. Pada versi awal, jumlah data per kelas sekitar puluhan hingga ratusan gambar dan dapat ditambah pada pengembangan berikutnya.

### 3.3 Perancangan Metode
Alur proses: input gambar -> preprocessing (resize, normalisasi) -> YOLOS -> output bounding box, label kelas, dan confidence. Konfigurasi training mencakup jumlah epoch, learning rate, batch size, optimizer AdamW, dan scheduler StepLR. Evaluasi menggunakan IoU, precision, recall, dan mAP. Format respons API mengembalikan daftar objek terdeteksi beserta bounding box dan skor.

### 3.4 Perancangan UML
Diagram UML (Use Case, Activity, Sequence, Class) disiapkan dalam folder `uml/` menggunakan format Mermaid.
