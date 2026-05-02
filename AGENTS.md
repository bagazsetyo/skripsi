
## BAB 1 — PENDAHULUAN

### 1.1 Latar Belakang

* Jelaskan pentingnya rambu lalu lintas untuk keselamatan dan ketertiban jalan.
* Jelaskan kebutuhan sistem otomatis untuk **deteksi** (lokasi rambu) dan **klasifikasi** (jenis rambu).
* Jelaskan tantangan pada citra jalan: rambu kecil, variasi pencahayaan, blur, sudut kamera, tertutup objek lain, latar ramai.
* Jelaskan alasan memilih **Vision Transformer (YOLOS)** untuk deteksi objek (bukan CNN tradisional).
* Jelaskan gambaran dataset rambu Indonesia yang digunakan dan potensi penerapannya.

---

➢ **Rumusan Masalah**
Tentukan masalah berdasarkan latar belakang. Contoh:

1. Bagaimana menerapkan **Vision Transformer (YOLOS)** untuk melakukan deteksi dan klasifikasi rambu lalu lintas Indonesia pada citra jalan?
2. Bagaimana performa model YOLOS pada dataset rambu Indonesia berdasarkan metrik evaluasi deteksi objek?
3. Bagaimana merancang sistem berbasis web untuk proses training, manajemen model, dan prediksi rambu lalu lintas?

---

➢ **Tujuan**
Tujuan adalah langkah untuk menjawab rumusan masalah. Contoh:

1. Membangun model deteksi dan klasifikasi rambu menggunakan **YOLOS (Vision Transformer)**.
2. Melakukan pelatihan model pada dataset rambu lalu lintas Indonesia serta melakukan evaluasi performa.
3. Mengembangkan aplikasi web (FastAPI–React) untuk upload gambar, menampilkan hasil deteksi, serta pengelolaan model hasil training.

---

➢ **Batasan Masalah**
Agar tidak terlalu luas, contoh batasannya:

1. Data yang digunakan adalah dataset rambu lalu lintas Indonesia (format anotasi bounding box).
2. Input berupa gambar statis (bukan video real-time).
3. Output sistem berupa bounding box, label kelas rambu, dan nilai confidence.
4. Pelatihan model dilakukan menggunakan konfigurasi terbatas (mis. jumlah epoch tertentu) menyesuaikan perangkat yang tersedia.
5. Penelitian tidak membahas tracking objek, OCR detail teks rambu, atau interpretasi aturan lalu lintas lanjutan.

---

➢ **Metodologi**
Tuliskan langkah penelitian agar tujuan tercapai. Contoh alur:

1. Studi literatur (deteksi rambu, transformer untuk object detection, YOLOS).
2. Pengumpulan dataset rambu lalu lintas Indonesia.
3. Preprocessing data (resize, normalisasi, konversi label bbox bila diperlukan).
4. Implementasi model **YOLOS** dan penyesuaian jumlah kelas.
5. Training model dan penyimpanan model + riwayat training.
6. Evaluasi model (IoU, precision, recall, mAP).
7. Integrasi model ke aplikasi web (FastAPI backend + React frontend).
8. Pengujian sistem end-to-end dan analisis hasil.
9. Penyusunan laporan dan kesimpulan.

---

## BAB 2 — LANDASAN TEORI / TINJAUAN PUSTAKA

**Tuliskan materi-materi yang berhubungan dengan topik KP/Skripsi.**
Tambahkan hasil penelitian sejenis untuk perbandingan dan pembeda.
Jika mengutip pustaka, beri sitasi format **IEEE** (sesuai format USB).
Teori dijelaskan lengkap: minimal 1 halaman per materi, dan teori metode minimal 2–3 halaman.

### 2.1 Konsep Dasar Deteksi Objek

* Definisi deteksi objek dan perbedaan dengan klasifikasi.
* Konsep bounding box, label kelas, confidence score.

### 2.2 Rambu Lalu Lintas dan Karakteristik Objek Rambu

* Jenis rambu (larangan, perintah, peringatan, petunjuk) dan contoh.
* Tantangan rambu sebagai objek kecil pada citra jalan.

### 2.3 Dataset Rambu Lalu Lintas Indonesia

* Struktur data train/test, kelas-kelas rambu, format anotasi bounding box.
* Distribusi jumlah data per kelas (nanti bisa tabel).

### 2.4 Vision Transformer (ViT)

* Konsep patch embedding.
* Self-attention dan kemampuan menangkap konteks global.
* Kelebihan/kekurangan transformer dibanding CNN dalam visi komputer.

### 2.5 Metode YOLOS (You Only Look at One Sequence)

*(Bagian ini minimal 2–3 halaman karena ini metode utama)*

* Konsep YOLOS sebagai transformer untuk object detection.
* Representasi input (patch + token), prediksi bbox dan kelas.
* Cara kerja training dan inference secara ringkas (sesuai library yang dipakai).
* Alasan pemilihan YOLOS untuk kasus deteksi rambu.

### 2.6 Metrik Evaluasi Deteksi Objek

* IoU (Intersection over Union).
* Precision, Recall.
* mAP (mis. mAP@0.5 atau mAP@0.5:0.95).

### 2.7 Teknologi yang Digunakan

* Python (training & inference)
* Framework/Library (mis. PyTorch + HuggingFace Transformers untuk YOLOS)
* FastAPI (backend)
* React (frontend)
* Docker (deployment)
* SQLite (opsional: penyimpanan riwayat training dan model registry)

### 2.8 Penelitian Terkait

* Ringkas beberapa penelitian deteksi rambu (YOLO, SSD, Faster R-CNN) sebagai pembanding.
* Ringkas penelitian object detection berbasis transformer (DETR/YOLOS) sebagai pembeda.
* Buat tabel perbandingan (opsional): metode, dataset, hasil, gap, kontribusi kamu.

---

## BAB 3 — PERANCANGAN

*(Merupakan bab perancangan yang terdiri dari poin wajib berikut)*

✓ **3.1 Metodologi Penelitian**

* Uraikan lagi alur penelitian (boleh lebih detail dari Bab 1).
* Buat diagram alur (flowchart) dari dataset → preprocessing → training → evaluasi → integrasi sistem.

✓ **3.2 Data-data Penelitian**

* Sumber dataset rambu Indonesia.
* Struktur folder train/test.
* Daftar kelas rambu yang digunakan (dengan kode/label).
* Contoh format anotasi bbox.
* Pembagian data (train/val/test) dan alasan pembagian.
* (Opsional) Augmentasi data yang digunakan.

✓ **3.3 Perancangan Metode**

* Rancangan pipeline YOLOS:

  * input image size
  * preprocessing
  * konfigurasi model (variant YOLOS)
  * jumlah kelas
  * loss / optimizer / hyperparameter (lr, batch size, epoch)
* Rancangan proses training:

  * penyimpanan checkpoint/model
  * pencatatan history training
* Rancangan proses inference:

  * threshold confidence
  * output bbox + label
* Rancangan evaluasi:

  * IoU, precision/recall, mAP
  * skenario pengujian (per kelas dan keseluruhan)

✓ **3.4 Perancangan UML**
Minimal yang umum dipakai:

* Use Case Diagram (aktor: Admin, User)
* Activity Diagram (proses training & proses prediksi)
* Sequence Diagram (upload → backend → model → response)
* Class Diagram (opsional) untuk struktur modul

Contoh use case:

* Admin: scan dataset, pilih kelas, train model, lihat history, aktifkan model
* User: upload gambar, lihat hasil deteksi

✓ **3.5 Perancangan Mock-up**