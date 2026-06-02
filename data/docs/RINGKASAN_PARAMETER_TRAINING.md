# Ringkasan Parameter Training

Dokumen ini berisi ringkasan parameter training dengan bahasa yang mudah dipahami. Tujuannya agar bisa dipakai saat:
- bimbingan
- penulisan Bab 3 dan Bab 4
- persiapan sidang

## 1. Epochs

`Epochs` adalah jumlah pengulangan saat model mempelajari seluruh data training.

Penjelasan sederhana:
- jika `epochs = 1`, berarti model melihat seluruh data training satu kali
- jika `epochs = 30`, berarti model melihat seluruh data training sebanyak 30 kali

Pengaruh:
- terlalu kecil: model bisa belum belajar cukup
- terlalu besar: model bisa terlalu hafal data training

Kalimat aman:

> Epochs menunjukkan jumlah pengulangan model dalam mempelajari seluruh data training.

## 2. Batch Size

`Batch size` adalah jumlah gambar yang diproses sekaligus dalam satu langkah training.

Penjelasan sederhana:
- `batch size = 1` berarti model memproses 1 gambar setiap langkah update
- `batch size = 2` berarti model memproses 2 gambar sekaligus setiap langkah update

Hal penting:
- batch size **bukan** jumlah pengulangan belajar
- yang menentukan berapa kali seluruh data dipelajari adalah `epochs`

Pengaruh:
- batch size lebih besar biasanya membutuhkan memori GPU lebih besar
- batch size kecil lebih aman untuk GPU terbatas

Kalimat aman:

> Batch size menunjukkan jumlah sampel yang diproses sekaligus dalam satu langkah pelatihan.

## 3. Image Size

`Image size` adalah ukuran gambar input yang diberikan ke model.

Penjelasan sederhana:
- gambar akan disesuaikan ukurannya sebelum diproses model
- ukuran yang lebih besar memberi detail visual lebih banyak

Pengaruh:
- ukuran lebih besar bisa membantu mendeteksi objek kecil
- tetapi ukuran lebih besar membuat training lebih berat dan lebih lambat

Kalimat aman:

> Image size memengaruhi banyaknya detail visual yang diterima model dan berpengaruh terhadap kemampuan deteksi objek kecil.

## 4. Learning Rate

`Learning rate` adalah besar langkah model saat memperbarui bobot.

Penjelasan sederhana:
- learning rate besar: model belajar dengan langkah lebih besar
- learning rate kecil: model belajar lebih hati-hati

Pengaruh:
- terlalu besar: training bisa tidak stabil
- terlalu kecil: training bisa sangat lambat

Kalimat aman:

> Learning rate mengatur seberapa besar perubahan bobot model pada setiap langkah pelatihan.

## 5. Weight Decay

`Weight decay` adalah parameter regularisasi untuk membantu model agar tidak terlalu overfit pada data training.

Penjelasan sederhana:
- model dibatasi agar tidak terlalu menyesuaikan diri secara berlebihan terhadap data training

Pengaruh:
- membantu menjaga model tetap lebih umum
- biasanya nilainya kecil

Kalimat aman:

> Weight decay digunakan untuk membantu mengontrol kompleksitas model agar tidak terlalu menyesuaikan diri pada data training.

## 6. Score Threshold

`Score threshold` adalah batas minimum confidence agar hasil deteksi ditampilkan.

Penjelasan sederhana:
- jika confidence model di bawah threshold, hasil deteksi tidak ditampilkan
- jika confidence di atas threshold, hasil deteksi akan muncul

Pengaruh:
- threshold tinggi: hasil lebih ketat, tetapi objek kecil bisa tidak muncul
- threshold rendah: hasil lebih banyak muncul, tetapi false positive bisa bertambah

Catatan:
- parameter ini lebih berpengaruh saat evaluasi dan inferensi
- bukan parameter inti pembelajaran seperti epochs atau learning rate

Kalimat aman:

> Score threshold digunakan untuk menyaring hasil prediksi berdasarkan tingkat keyakinan model.

## 7. Kenapa Pengujian Utama Fokus pada Image Size

Pada pengujian utama Bab 4, fokus diarahkan ke `image size`.

Alasannya:
- dosen meminta perbandingan ukuran input gambar
- jika semua parameter diubah sekaligus, hasil sulit dianalisis
- dengan menjaga parameter lain tetap, pengaruh `image size` bisa terlihat lebih jelas

Kalimat aman:

> Pada pengujian utama, parameter lain dijaga tetap agar pengaruh image size terhadap performa model dapat diamati secara lebih jelas.

## 8. Kenapa Batch Size Tidak Dinaikkan

Batch size tidak dinaikkan pada pengujian utama karena:
- fokus pengujian bukan pada batch size
- image size yang lebih besar membutuhkan memori GPU lebih besar
- batch size 1 lebih aman agar eksperimen tidak gagal karena kehabisan memori

Kalimat aman:

> Batch size dipertahankan agar eksperimen tetap konsisten dan untuk menghindari keterbatasan memori GPU saat ukuran input gambar diperbesar.

## 9. Ringkasan Singkat untuk Hafalan

- `Epochs`: berapa kali seluruh data dipelajari
- `Batch size`: berapa banyak gambar diproses sekaligus
- `Image size`: ukuran gambar input ke model
- `Learning rate`: besar langkah update bobot
- `Weight decay`: regularisasi agar tidak overfit
- `Score threshold`: batas confidence hasil deteksi

## 10. Penjelasan Sangat Singkat untuk Sidang

Jika butuh versi paling singkat:

- `Epochs` menjelaskan berapa kali seluruh data training dipelajari model
- `Batch size` menjelaskan berapa banyak data yang diproses sekaligus dalam satu langkah
- `Image size` menjelaskan ukuran input gambar ke model
- `Learning rate` mengatur besar langkah pembaruan bobot
- `Weight decay` membantu mengurangi risiko overfitting
- `Score threshold` menyaring hasil deteksi berdasarkan confidence
