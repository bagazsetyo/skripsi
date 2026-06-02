# Template Bab 4 - Pengujian Model

Dokumen ini adalah template awal untuk menyusun bagian pengujian model pada Bab 4. Isi yang masih berupa placeholder bisa diganti setelah hasil training dari Google Colab sudah tersedia.

## 4.X Pengujian Model Deteksi dan Klasifikasi Rambu Lalu Lintas

Pada tahap ini dilakukan pengujian model deteksi dan klasifikasi rambu lalu lintas Indonesia menggunakan pendekatan Vision Transformer, yaitu YOLOS. Pengujian dilakukan untuk mengetahui pengaruh konfigurasi training terhadap performa model dalam mendeteksi lokasi rambu dan mengklasifikasikan jenis rambu lalu lintas.

Proses training model pada penelitian ini dilakukan menggunakan **Google Colab** karena kebutuhan komputasi untuk pelatihan model YOLOS cukup besar, terutama saat dilakukan beberapa percobaan konfigurasi. Model hasil training kemudian diintegrasikan kembali ke aplikasi utama untuk keperluan pengujian dan demonstrasi sistem.

## 4.X.1 Tujuan Pengujian

Tujuan pengujian model pada penelitian ini adalah:

1. mengetahui pengaruh ukuran input gambar (`image size`) terhadap performa model
2. membandingkan hasil beberapa konfigurasi model
3. menentukan model terbaik yang akan digunakan pada aplikasi final
4. menganalisis hubungan antara konfigurasi training dan hasil deteksi rambu lalu lintas

## 4.X.2 Skenario Pengujian

Pengujian utama pada penelitian ini difokuskan pada perbandingan parameter **image size**. Parameter lain dijaga tetap agar perbedaan hasil benar-benar berasal dari perubahan ukuran input gambar.

Konfigurasi tetap yang digunakan adalah sebagai berikut:

- `epochs = 30`
- `batch_size = 1`
- `learning_rate = 0.00005`
- `weight_decay = 0.0001`
- `score_threshold = 0.5`

Sedangkan parameter yang dibandingkan adalah:

- `image_size = 500`
- `image_size = 600`
- `image_size = 700`

Jika diperlukan, pengujian tambahan dapat dilakukan pada parameter lain seperti `learning rate` atau `score threshold`, tetapi pengujian utama pada penelitian ini tetap difokuskan pada perbandingan `image size`.

## 4.X.3 Lingkungan Pengujian

Pengujian model dilakukan menggunakan lingkungan komputasi sebagai berikut:

| Komponen | Keterangan |
|---|---|
| Platform training | Google Colab |
| Framework | PyTorch |
| Model | YOLOS / Vision Transformer |
| Bahasa pemrograman | Python |
| Dataset | Dataset rambu lalu lintas Indonesia |
| Format anotasi | YOLO bounding box |

Tambahkan detail final sesuai kondisi sebenarnya, misalnya:

- jenis GPU Colab yang digunakan
- lama waktu training tiap model
- jumlah data train dan test

## 4.X.4 Konfigurasi Pengujian

Tabel berikut digunakan untuk mencatat konfigurasi tiap model yang diuji.

| No | Nama Run | Image Size | Epochs | Batch Size | Learning Rate | Weight Decay | Score Threshold |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | Model A | 500 | 30 | 1 | 0.00005 | 0.0001 | 0.5 |
| 2 | Model B | 600 | 30 | 1 | 0.00005 | 0.0001 | 0.5 |
| 3 | Model C | 700 | 30 | 1 | 0.00005 | 0.0001 | 0.5 |

Paragraf narasi yang bisa dipakai:

> Berdasarkan skenario pengujian yang telah ditetapkan, penelitian ini membandingkan tiga konfigurasi model dengan ukuran input gambar yang berbeda, yaitu 500, 600, dan 700 piksel. Parameter lain seperti epoch, batch size, learning rate, weight decay, dan score threshold dijaga tetap agar pengaruh image size terhadap performa model dapat diamati dengan lebih jelas.

### Perbandingan Konfigurasi Antar Model

Bagian ini penting untuk menjawab pertanyaan dosen seperti:
- apa yang berubah dari model 500 ke 600?
- apa yang tetap?
- kenapa hasilnya berbeda?

Tabel berikut bisa dipakai:

| Aspek | Model 500 | Model 600 | Model 700 | Keterangan |
|---|---|---|---|---|
| Image Size | 500 | 600 | 700 | Parameter utama yang dibandingkan |
| Epochs | 30 | 30 | 30 | Tetap |
| Batch Size | 1 | 1 | 1 | Tetap agar aman terhadap memori GPU |
| Learning Rate | 0.00005 | 0.00005 | 0.00005 | Tetap |
| Weight Decay | 0.0001 | 0.0001 | 0.0001 | Tetap |
| Score Threshold | 0.5 | 0.5 | 0.5 | Tetap |

Narasi yang bisa dipakai:

> Pada pengujian ini, hanya parameter image size yang diubah, yaitu 500, 600, dan 700 piksel. Parameter lain seperti epoch, batch size, learning rate, weight decay, dan score threshold dijaga tetap. Dengan demikian, perbedaan hasil evaluasi yang diperoleh dapat dianalisis sebagai pengaruh dari perubahan ukuran input gambar.

### Penjelasan Perubahan dari 500 ke 600 ke 700

Template penjelasan:

- **Model 500**
  - ukuran input lebih kecil
  - kebutuhan komputasi lebih ringan
  - waktu training cenderung lebih cepat
  - risiko: objek kecil bisa kurang terlihat jelas

- **Model 600**
  - ukuran input menengah
  - detail visual lebih baik dibanding model 500
  - beban komputasi meningkat dibanding model 500
  - sering menjadi titik tengah antara akurasi dan efisiensi

- **Model 700**
  - ukuran input paling besar di antara tiga percobaan
  - detail objek kecil berpotensi paling baik
  - waktu training dan kebutuhan memori paling tinggi
  - belum tentu selalu terbaik jika data atau proses training kurang stabil

Kalimat aman:

> Secara umum, peningkatan image size dari 500 ke 600 dan 700 diharapkan memberikan detail visual yang lebih baik kepada model. Namun, peningkatan ukuran input juga meningkatkan kebutuhan komputasi, sehingga perlu diamati apakah peningkatan akurasi yang diperoleh sebanding dengan biaya komputasi tambahan.

## 4.X.5 Hasil Pengujian

Tabel berikut digunakan untuk mencatat hasil evaluasi tiap model.

| No | Nama Run | Loss Akhir | Precision | Recall | mAP@0.5 | Mean IoU | Waktu Training | Keterangan |
|---|---|---:|---:|---:|---:|---:|---|---|
| 1 | Model A | - | - | - | - | - | - | - |
| 2 | Model B | - | - | - | - | - | - | - |
| 3 | Model C | - | - | - | - | - | - | - |

Paragraf narasi yang bisa dipakai:

> Setelah proses training selesai, masing-masing model dievaluasi menggunakan data pengujian untuk memperoleh nilai loss akhir, precision, recall, mAP@0.5, dan mean IoU. Hasil pengujian ini digunakan untuk menentukan konfigurasi model yang memberikan performa terbaik pada deteksi dan klasifikasi rambu lalu lintas Indonesia.

### Tabel Perbandingan Dampak Perubahan Image Size

Tabel ini dipakai untuk menulis hasil observasi perubahan dari 500 ke 600 ke 700.

| Aspek yang Diamati | Model 500 | Model 600 | Model 700 | Kesimpulan |
|---|---|---|---|---|
| Waktu training | - | - | - | - |
| Loss akhir | - | - | - | - |
| Precision | - | - | - | - |
| Recall | - | - | - | - |
| mAP@0.5 | - | - | - | - |
| Mean IoU | - | - | - | - |
| Deteksi objek kecil | - | - | - | - |

Narasi yang bisa dipakai:

> Berdasarkan tabel perbandingan, setiap kenaikan image size memberikan perubahan terhadap performa model maupun kebutuhan komputasi. Oleh karena itu, analisis tidak hanya berfokus pada satu nilai metrik, tetapi juga mempertimbangkan kestabilan hasil dan efisiensi proses training.

## 4.X.6 Analisis Hasil Pengujian

Bagian ini berisi pembahasan hasil, bukan hanya menampilkan angka.

Template analisis:

> Berdasarkan hasil pengujian, model dengan image size [isi ukuran terbaik] menunjukkan performa yang paling baik dibandingkan konfigurasi lainnya. Hal ini terlihat dari nilai [isi metrik utama] yang lebih tinggi dibandingkan model lain. Peningkatan ukuran input gambar membantu model menangkap detail visual rambu, terutama pada objek yang berukuran kecil atau berada pada jarak yang lebih jauh.

> Namun demikian, peningkatan image size juga berdampak pada meningkatnya kebutuhan komputasi dan waktu training. Model dengan ukuran input yang lebih besar membutuhkan proses pelatihan yang lebih lama dibandingkan model dengan ukuran input yang lebih kecil. Oleh karena itu, pemilihan model terbaik tidak hanya mempertimbangkan akurasi, tetapi juga efisiensi komputasi.

> Pada penelitian ini, model [isi nama model terbaik] dipilih sebagai model terbaik karena memberikan keseimbangan yang paling baik antara performa deteksi dan efisiensi proses training.

### Template Analisis Perubahan Antar Konfigurasi

Bagian ini bisa ditulis lebih eksplisit agar terlihat benar-benar membandingkan 500, 600, dan 700.

#### Perbandingan Model 500 dan Model 600

Template:

> Dibandingkan model 500, model 600 menunjukkan [isi peningkatan/penurunan] pada metrik [isi metrik]. Hal ini mengindikasikan bahwa penambahan ukuran input dari 500 menjadi 600 memberikan [isi dampak], terutama pada [isi kondisi, misalnya objek kecil atau detail rambu].

#### Perbandingan Model 600 dan Model 700

Template:

> Dibandingkan model 600, model 700 menunjukkan [isi peningkatan/penurunan] pada metrik [isi metrik]. Meskipun ukuran input lebih besar berpotensi memberikan detail visual yang lebih baik, peningkatan ini juga disertai dengan [isi dampak, misalnya waktu training lebih lama atau kebutuhan komputasi lebih tinggi].

#### Kesimpulan Perbandingan 500, 600, dan 700

Template:

> Berdasarkan ketiga konfigurasi yang diuji, dapat dilihat bahwa perubahan image size memengaruhi performa model secara nyata. Model dengan ukuran input yang lebih besar tidak selalu otomatis menjadi yang terbaik, karena hasil akhir tetap dipengaruhi oleh kualitas data, kestabilan proses training, dan efisiensi komputasi.

### Template analisis per model

#### Model A

- kelebihan:
  - [isi]
- kekurangan:
  - [isi]
- kesimpulan singkat:
  - [isi]

#### Model B

- kelebihan:
  - [isi]
- kekurangan:
  - [isi]
- kesimpulan singkat:
  - [isi]

#### Model C

- kelebihan:
  - [isi]
- kekurangan:
  - [isi]
- kesimpulan singkat:
  - [isi]

## 4.X.7 Pemilihan Model Terbaik

Template narasi:

> Berdasarkan seluruh hasil pengujian, model terbaik yang dipilih untuk diintegrasikan ke aplikasi adalah **[isi nama model]**. Pemilihan ini dilakukan karena model tersebut memiliki performa paling baik berdasarkan metrik evaluasi, khususnya pada [isi metrik utama], serta memberikan hasil deteksi yang lebih konsisten pada data uji maupun pengujian visual menggunakan gambar/video.

Tambahkan tabel ringkas jika perlu:

| Kriteria | Model Terpilih | Alasan |
|---|---|---|
| Akurasi terbaik | - | - |
| Waktu training paling efisien | - | - |
| Paling stabil untuk demo | - | - |

## 4.X.8 Pengujian Visual pada Gambar dan Video

Selain menggunakan metrik kuantitatif, model terbaik juga diuji secara visual pada gambar statis dan video. Pengujian ini bertujuan untuk melihat kemampuan model dalam mendeteksi rambu lalu lintas secara langsung pada kondisi yang lebih mendekati penggunaan nyata.

Template narasi:

> Hasil pengujian visual menunjukkan bahwa model mampu mendeteksi beberapa jenis rambu lalu lintas dengan cukup baik pada gambar statis maupun video. Namun, performa model dapat menurun pada objek rambu yang berukuran kecil, terlalu jauh, atau berada dalam kondisi pencahayaan yang kurang baik. Hal ini menunjukkan bahwa selain parameter training, karakteristik data dan ukuran objek juga sangat memengaruhi hasil deteksi.

Jika perlu, tambahkan subbagian:

### a. Pengujian pada gambar statis
- [isi hasil]

### b. Pengujian pada video / near real-time
- [isi hasil]

## 4.X.9 Kesimpulan Pengujian Model

Template narasi:

> Berdasarkan pengujian yang telah dilakukan, dapat disimpulkan bahwa variasi ukuran input gambar berpengaruh terhadap performa model YOLOS dalam mendeteksi dan mengklasifikasikan rambu lalu lintas Indonesia. Model dengan konfigurasi **[isi model terbaik]** memberikan hasil paling baik dan dipilih untuk digunakan pada implementasi akhir aplikasi. Meskipun demikian, masih terdapat keterbatasan pada deteksi objek rambu yang kecil atau berada dalam kondisi visual yang kurang ideal.

## Catatan Pengisian

Saat hasil training dari Google Colab sudah tersedia, isi bagian berikut terlebih dahulu:

1. tabel konfigurasi pengujian
2. tabel hasil pengujian
3. model terbaik yang dipilih
4. analisis perbedaan hasil antar image size
5. hasil pengujian visual pada gambar dan video

## Saran Alur Kerja

Urutan yang disarankan:

1. training 3 model di Google Colab
2. catat hasil metrik tiap model
3. isi tabel hasil pengujian
4. pilih model terbaik
5. uji model terbaik di aplikasi
6. isi bagian analisis dan kesimpulan Bab 4
