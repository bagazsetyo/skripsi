# Hasil Perbandingan Model — YOLOS-small (img500 / img600 / img700)

## 1. Gambaran Umum

Tiga model dilatih dengan kondisi yang **persis sama** — cara belajar, durasi, data, dan
seluruh konfigurasi identik. Satu-satunya perbedaan adalah **ukuran gambar input**:

| Model | Ukuran Gambar |
|-------|--------------|
| Model A | 500 px |
| Model B | 600 px |
| Model C | 700 px |

Tujuannya: mengetahui apakah gambar yang lebih besar membuat model lebih akurat dalam
mengenali rambu lalu lintas.

---

## 2. Konfigurasi Training (Identik)

| Parameter | img500 | img600 | img700 |
|-----------|--------|--------|--------|
| Epochs | 40 | 40 | 40 |
| Batch Size | 2 | 2 | 2 |
| Learning Rate | 5×10⁻⁵ | 5×10⁻⁵ | 5×10⁻⁵ |
| LR Warmup | 4 epoch | 4 epoch | 4 epoch |
| LR Scheduler | Cosine Decay | Cosine Decay | Cosine Decay |
| Weight Decay | 0.0001 | 0.0001 | 0.0001 |
| Gradient Clipping | 0.1 | 0.1 | 0.1 |
| Mixed Precision | Ya (AMP) | Ya (AMP) | Ya (AMP) |
| GPU | A100 80 GB | A100 80 GB | A100 80 GB |
| Dataset | 5.494 train / 540 test | sama | sama |

Karena semua kondisi identik, perbedaan hasil yang muncul **murni disebabkan oleh
perbedaan ukuran gambar input** — bukan faktor lain.

---

## 3. Hasil Keseluruhan

| Model | mAP@0.5 | Precision | Recall | Mean IoU | Waktu Latih |
|-------|---------|-----------|--------|----------|-------------|
| img500 | 90.27% | 89.79% | 91.23% | 90.67% | 8.77 jam |
| **img600** | **92.07%** | **94.16%** | **92.31%** | 90.71% | 8.75 jam |
| img700 | 90.83% | 92.24% | 91.41% | **91.22%** | 8.78 jam |

**Peringkat: img600 > img700 > img500**

Yang menarik: waktu latih ketiganya hampir sama persis (~8.75 jam), meskipun ukuran
gambarnya berbeda jauh. Ini karena proses yang paling memakan waktu bukan komputasi
model, melainkan proses baca-tulis data dari disk (*I/O bottleneck*).

---

## 4. Hasil per Kelas

| Kelas | img500 | img600 | img700 | Terbaik |
|-------|--------|--------|--------|---------|
| larangan-berhenti | 86.5% | 90.0% | 86.5% | img600 |
| larangan-masuk-bagi-kendaraan | 80.0% | 90.0% | 90.0% | img600/700 |
| larangan-parkir | 61.1% | 68.2% | **75.5%** | img700 |
| larangan-belok-kanan | 90.3% | **93.4%** | 90.3% | img600 |
| larangan-belok-kiri | 94.0% | **97.1%** | 96.7% | img600 |
| larangan-berjalan-terus | **91.2%** | **91.2%** | 88.0% | img500/600 |
| larangan-memutar-balik | **66.1%** | 65.9% | 48.7% | img500 |
| peringatan-alat-pemberi-isyarat | **99.6%** | 96.6% | 90.0% | img500 |
| peringatan-banyak-pejalan-kaki | 97.2% | **100.0%** | **100.0%** | img600/700 |
| peringatan-pintu-perlintasan-kereta-api | **100.0%** | **100.0%** | **100.0%** | tie |
| peringatan-simpang-tiga-sisi-kiri | 96.7% | 93.3% | **100.0%** | img700 |
| peringatan-penegasan-rambu-tambahan | 99.8% | **100.0%** | **100.0%** | img600/700 |
| perintah-masuk-jalur-kiri | 72.3% | 81.7% | **89.2%** | img700 |
| perintah-pilihan-memasuki-salah-satu-jalur | **93.3%** | **93.3%** | 86.7% | img500/600 |
| petunjuk-area-parkir | **100.0%** | **100.0%** | **100.0%** | tie |
| petunjuk-lokasi-pemberhentian-bus | **100.0%** | **100.0%** | **100.0%** | tie |
| petunjuk-lokasi-putar-balik | **96.7%** | **96.7%** | **96.7%** | tie |
| petunjuk-penyeberangan-pejalan-kaki | **100.0%** | 99.9% | 96.7% | img500 |

---

## 5. Analisis: Kenapa img700 Tidak Lebih Baik dari img600?

Secara logika, gambar lebih besar seharusnya memberi lebih banyak detail sehingga model
lebih akurat. Namun pada kenyataannya, gambar yang terlalu besar justru bisa membuat
model kesulitan karena harus memproses lebih banyak bagian gambar sekaligus — sehingga
perhatiannya terpecah dan fokusnya berkurang.

Bukti paling jelas ada pada kelas **larangan-memutar-balik**:

| Model | Akurasi | FP | FN |
|-------|---------|----|----|
| img500 | 66.1% | 6 | 10 |
| img600 | 65.9% | 4 | 10 |
| img700 | **48.7%** | 2 | **15** |

img700 melewatkan 15 dari 30 rambu larangan memutar balik (recall hanya 50%) — jauh
lebih buruk dari dua model lainnya. Rambu ini bentuknya mirip dengan larangan-parkir
(keduanya bulat merah), dan resolusi yang lebih tinggi tidak membantu membedakannya;
justru sebaliknya.

---

## 6. Kelas yang Memang Butuh Gambar Lebih Besar

Tidak semua kelas lebih baik di resolusi rendah. Ada kelas yang memang memiliki detail
kecil sehingga gambar lebih besar membantu:

| Kelas | img500 | img600 | img700 | Keterangan |
|-------|--------|--------|--------|-----------|
| larangan-parkir | 61.1% | 68.2% | **75.5%** | Makin tinggi resolusi makin baik |
| perintah-masuk-jalur-kiri | 72.3% | 81.7% | **89.2%** | Makin tinggi resolusi makin baik |
| peringatan-simpang-tiga-sisi-kiri | 96.7% | 93.3% | **100.0%** | img700 sempurna |

Kedua kelas pertama memiliki detail visual yang perlu dilihat lebih dekat — seperti
arah panah dan pola jalur — sehingga gambar yang lebih besar memberikan manfaat nyata.

---

## 7. Apakah Perlu Menambah Model 800px atau 900px?

**Tidak perlu.**

Tiga alasan utama:

1. **Tren sudah jelas.** Dari data 500 → 600 → 700, terlihat bahwa setelah 600px
   performanya tidak meningkat secara keseluruhan. Menambah 800px atau 900px
   kemungkinan besar akan mengikuti pola yang sama atau lebih buruk.

2. **Risiko VRAM.** img700 sudah menggunakan ~46–50 GB dari 80 GB VRAM yang tersedia.
   img800 ke atas kemungkinan perlu menurunkan batch size, yang akan membuat kondisi
   training tidak lagi identik dan hasil perbandingan menjadi tidak adil.

3. **Tiga titik data sudah cukup** untuk sebuah penelitian skripsi. Temuan yang ada
   sudah bermakna dan dapat dipertanggungjawabkan secara ilmiah.

---

## 8. Kesimpulan

> **img600 adalah model terbaik** dengan mAP 92.07%, precision 94.16%, dan performa
> paling seimbang di 18 kelas.

> Menambah ukuran gambar dari 600px ke 700px **tidak meningkatkan akurasi secara
> keseluruhan** — bahkan menurunkannya pada beberapa kelas penting. Ini menunjukkan
> bahwa pada dataset rambu lalu lintas ini, terdapat *optimal resolution point* di
> sekitar 600px.

> Selisih antara ketiga model relatif kecil (±2%), yang berarti ketiga model sudah
> mampu belajar dengan baik dari data yang ada. Perbedaan utama terletak pada
> kemampuan membedakan kelas-kelas yang secara visual mirip satu sama lain.

### Rekomendasi untuk Deployment

Model yang direkomendasikan untuk digunakan pada sistem inferensi adalah
**YOLOS-small img600**, karena memberikan keseimbangan terbaik antara akurasi,
kecepatan inferensi, dan konsumsi memori.
