# Bab 4 - Pengujian Model dan Pedoman Training

Dokumen ini dipakai sebagai:
- pedoman melakukan training model
- acuan menyusun bagian pengujian model pada Bab 4
- panduan menentukan parameter mana yang dibandingkan dan mana yang dijaga tetap

## 1. Tujuan Pengujian

Pengujian pada Bab 4 bertujuan untuk melihat pengaruh konfigurasi training terhadap performa model deteksi rambu lalu lintas Indonesia berbasis YOLOS. Fokus utama pengujian yang diminta dosen saat ini adalah **perbandingan ukuran input gambar (`image size`)**.

Selain itu, dokumen ini juga menjelaskan parameter lain yang tersedia pada sistem:
- `Epochs`
- `Batch Size`
- `Image Size`
- `Learning Rate`
- `Weight Decay`
- `Score Threshold`

Namun, agar hasil pengujian valid dan mudah dianalisis, **tidak semua parameter perlu diubah sekaligus**.

## 2. Prinsip Pengujian yang Benar

Prinsip utama pengujian adalah:

**ubah satu variabel utama, lalu variabel lain dijaga tetap**

Artinya:
- jika yang dibandingkan adalah `image size`, maka:
  - `epochs` tetap
  - `batch size` tetap
  - `learning rate` tetap
  - `weight decay` tetap
  - `score threshold` tetap

Tujuannya agar perbedaan hasil benar-benar berasal dari ukuran input gambar, bukan dari perubahan banyak parameter sekaligus.

## 3. Apakah Semua Parameter Perlu Diubah?

### Jawaban singkat

**Tidak perlu semuanya diubah untuk Bab 4 utama.**

Yang paling aman:
- jadikan `image size` sebagai **pengujian utama**
- parameter lain dijaga tetap

### Alasan

Kalau semua parameter diubah sekaligus:
- hasil jadi sulit dianalisis
- sulit menjawab pertanyaan dosen "kenapa model ini lebih baik?"
- sulit menyimpulkan faktor penyebab perubahan akurasi

### Rekomendasi

Untuk Bab 4 utama:
- **wajib** bandingkan `image size`
- **opsional** jika ada waktu:
  - bandingkan `learning rate`
  - bandingkan `score threshold` saat pengujian inferensi

Parameter lain seperti `batch size`, `weight decay`, dan `epochs` sebaiknya **tetap dulu**, kecuali ada alasan eksperimen khusus.

## 4. Penjelasan Tiap Parameter

### 4.1 Epochs

`Epochs` adalah jumlah pengulangan training terhadap seluruh data latih.

Pengaruh:
- makin besar epoch, model punya kesempatan belajar lebih lama
- terlalu sedikit epoch dapat membuat model belum belajar optimal
- terlalu banyak epoch dapat menyebabkan overfitting

Saran untuk pengujian utama:
- **tetap**
- gunakan nilai yang sama untuk semua percobaan

Rekomendasi awal:
- `30`

### 4.2 Batch Size

`Batch Size` adalah jumlah gambar yang diproses dalam satu langkah training.

Pengaruh:
- batch lebih besar bisa membuat training lebih stabil
- tetapi batch lebih besar juga membutuhkan VRAM lebih besar
- pada GPU terbatas, batch size sering menjadi penyebab OOM

Saran untuk pengujian utama:
- **tetap**
- pilih nilai yang aman agar semua eksperimen bisa jalan

Rekomendasi awal:
- `1`

Catatan:
- untuk `image size` yang besar seperti `700`, `batch size 1` adalah pilihan paling aman

### 4.3 Image Size

`Image Size` adalah ukuran input gambar yang diberikan ke model.

Pengaruh:
- ukuran lebih besar biasanya membantu objek kecil lebih terlihat
- tetapi ukuran lebih besar membuat:
  - penggunaan VRAM naik
  - waktu training lebih lama
  - waktu inferensi lebih lambat

Inilah parameter utama yang saat ini diminta untuk dibandingkan.

### 4.4 Learning Rate

`Learning Rate` mengatur seberapa besar langkah model saat memperbarui bobot.

Pengaruh:
- terlalu besar: training bisa tidak stabil
- terlalu kecil: training sangat lambat dan bisa kurang optimal

Saran untuk pengujian utama:
- **tetap**

Rekomendasi awal:
- `0.00005`

Catatan:
- nilai `0.0001` masih bisa dipakai
- tetapi untuk dataset yang tidak terlalu besar, `0.00005` biasanya lebih stabil

### 4.5 Weight Decay

`Weight Decay` membantu regularisasi model agar tidak terlalu overfit.

Pengaruh:
- terlalu kecil: regularisasi lemah
- terlalu besar: model bisa terlalu dibatasi

Saran untuk pengujian utama:
- **tetap**

Rekomendasi awal:
- `0.0001`

### 4.6 Score Threshold

`Score Threshold` adalah batas minimum confidence agar hasil deteksi ditampilkan.

Penting:
- ini **bukan inti training**
- ini lebih berpengaruh saat evaluasi dan inferensi

Pengaruh:
- threshold tinggi:
  - hasil lebih ketat
  - false positive berkurang
  - tetapi objek kecil bisa tidak tampil
- threshold rendah:
  - hasil lebih banyak muncul
  - recall bisa naik
  - tetapi false positive bisa bertambah

Saran untuk pengujian utama:
- **tetap**

Rekomendasi awal:
- `0.5`

Opsional:
- jika nanti ingin eksperimen tambahan, bisa bandingkan:
  - `0.3`
  - `0.4`
  - `0.5`

## 5. Rekomendasi Skenario Pengujian Utama Bab 4

Karena dosen meminta perbandingan `image size`, maka pengujian utama disarankan seperti ini:

## Skenario A - Perbandingan Image Size

Parameter yang dibandingkan:
- `image_size = 500`
- `image_size = 600`
- `image_size = 700`

Parameter lain dijaga tetap:
- `epochs = 30`
- `batch_size = 1`
- `learning_rate = 0.00005`
- `weight_decay = 0.0001`
- `score_threshold = 0.5`

Catatan penting:
- nilai `500`, `600`, `700` boleh dipakai karena itu yang diminta dosen
- tetapi jika nanti muncul masalah teknis atau kebutuhan penyesuaian model, alternatif yang lebih umum secara teknis adalah:
  - `512`
  - `640`
  - `704` atau `768`

Namun untuk konsistensi dengan arahan dosen, tahap awal disarankan tetap mencoba:
- `500`
- `600`
- `700`

## 6. Rekomendasi Skenario Tambahan Jika Masih Ada Waktu

Jika pengujian utama sudah selesai dan masih ada waktu, pengujian tambahan yang paling masuk akal adalah:

### Skenario B - Perbandingan Learning Rate

Tetap gunakan satu `image size` terbaik dari Skenario A, lalu bandingkan:
- `0.0001`
- `0.00005`
- `0.00003`

Parameter lain tetap:
- `epochs = 30`
- `batch_size = 1`
- `weight_decay = 0.0001`
- `score_threshold = 0.5`

### Skenario C - Perbandingan Score Threshold saat Inference

Ini bukan pengujian training inti, tetapi berguna untuk menunjukkan pengaruh threshold terhadap hasil deteksi video/gambar.

Bandingkan:
- `0.3`
- `0.4`
- `0.5`

Tujuannya:
- melihat apakah objek kecil lebih mudah tampil pada threshold yang lebih rendah

## 7. Skenario yang Tidak Disarankan untuk Sekarang

Agar waktu tidak habis, saat ini sebaiknya **hindari**:
- mengubah banyak parameter sekaligus
- mengubah `batch size` dan `image size` dalam eksperimen yang sama
- terlalu banyak kombinasi grid search
- langsung memakai ukuran sangat besar tanpa uji VRAM

Contoh yang tidak disarankan:
- eksperimen 3 image size x 3 learning rate x 3 batch size sekaligus

Itu akan terlalu banyak dan sulit selesai sebelum deadline.

## 8. Data yang Perlu Dicatat Saat Training

Setiap training minimal mencatat:
- nama run
- image size
- epochs
- batch size
- learning rate
- weight decay
- score threshold
- waktu training
- loss akhir
- precision
- recall
- mAP@0.5
- mean IoU

Jika memungkinkan, tambahkan:
- status berhasil / gagal
- catatan OOM atau error

## 9. Template Tabel Pengujian untuk Bab 4

### Tabel Konfigurasi Pengujian

| No | Nama Run | Image Size | Epochs | Batch Size | Learning Rate | Weight Decay | Score Threshold |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | Model A | 500 | 30 | 1 | 0.00005 | 0.0001 | 0.5 |
| 2 | Model B | 600 | 30 | 1 | 0.00005 | 0.0001 | 0.5 |
| 3 | Model C | 700 | 30 | 1 | 0.00005 | 0.0001 | 0.5 |

### Tabel Hasil Pengujian Model

| No | Nama Run | Loss Akhir | Precision | Recall | mAP@0.5 | Mean IoU | Keterangan |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | Model A | - | - | - | - | - | - |
| 2 | Model B | - | - | - | - | - | - |
| 3 | Model C | - | - | - | - | - | - |

### Tabel Hasil Analisis

| Model | Kelebihan | Kekurangan | Kesimpulan |
|---|---|---|---|
| Model A | - | - | - |
| Model B | - | - | - |
| Model C | - | - | - |

## 10. Pedoman Penulisan Analisis Bab 4

Saat menulis hasil pengujian, jangan hanya menulis angka. Tambahkan analisis seperti:

- model dengan image size lebih besar cenderung lebih baik dalam mendeteksi objek kecil
- tetapi image size yang lebih besar membutuhkan waktu training lebih lama
- jika image size terlalu besar, penggunaan memori meningkat
- model terbaik dipilih berdasarkan keseimbangan antara akurasi dan efisiensi

Contoh arah analisis:

> Berdasarkan hasil pengujian, ukuran input gambar memengaruhi performa model dalam mendeteksi rambu lalu lintas. Ukuran input yang lebih besar cenderung memberikan detail visual yang lebih baik, terutama pada objek rambu yang berukuran kecil atau berada pada jarak yang lebih jauh. Namun, peningkatan ukuran input juga meningkatkan kebutuhan komputasi dan waktu pemrosesan.

## 11. Rekomendasi Praktis untuk Training Sekarang

Jika ingin langsung mulai training Bab 4, gunakan urutan ini:

### Tahap 1 - Pengujian utama
- train model `image_size 500`
- train model `image_size 600`
- train model `image_size 700`

### Tahap 2 - Ambil model terbaik
- pilih model dengan hasil paling baik
- cek juga hasil deteksi pada gambar/video nyata

### Tahap 3 - Jika masih sempat
- bandingkan `learning rate`
- atau bandingkan `score threshold`

## 12. Kesimpulan Pedoman

Kesimpulan utama dokumen ini:

- untuk Bab 4 sekarang, **fokus utama cukup pada perbandingan image size**
- parameter lain **tidak perlu diubah dulu**, cukup dijaga tetap
- parameter lain baru diuji jika ada waktu tambahan
- pendekatan ini paling aman, paling mudah dianalisis, dan paling mudah dipertanggungjawabkan saat sidang
