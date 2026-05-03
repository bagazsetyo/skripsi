# Opsi Cloud GPU untuk Training Model

Dokumen ini merangkum opsi cloud GPU yang paling realistis untuk project skripsi ini per **3 Mei 2026**.

Fokus dokumen ini:
- setup tidak terlalu rumit
- cocok untuk stack saat ini: `Docker`, `PyTorch`, `FastAPI`, `React`
- bisa dipakai untuk training model YOLOS di repo ini
- ada gambaran harga untuk perbandingan

Catatan:
- harga cloud GPU bisa berubah sewaktu-waktu
- harga di bawah ini dipakai sebagai acuan awal, bukan angka final permanen
- untuk project ini, yang paling relevan adalah **training di container/backend**, bukan layanan inference serverless

## Rekomendasi Singkat

### Pilihan yang paling saya sarankan
1. **RunPod**
   Cocok jika ingin cepat jalan, dekat dengan workflow Docker sekarang, dan biaya relatif masuk akal.
2. **DigitalOcean Paperspace**
   Cocok jika ingin platform yang lebih rapi dan stabil, walau biasanya sedikit lebih mahal dibanding opsi termurah.

### Opsi yang saya sengaja tidak prioritaskan
- **Vast.ai**: sering murah, tapi pengalaman setup dan kualitas host lebih bervariasi.
- **AWS / Google Cloud**: sangat kuat, tapi untuk skripsi ini setup dan billing-nya lebih kompleks dari yang diperlukan.
- **Google Colab**: enak untuk eksperimen kecil, tetapi sesi, storage, dan konsistensi runtime kurang ideal untuk training model yang ingin diulang beberapa kali.

---

## 1. RunPod

### Kenapa cocok untuk project ini
- paling dekat dengan workflow lokal Anda
- bisa jalan dengan container GPU
- cocok untuk training berkali-kali dan menyimpan banyak model
- lebih mudah untuk pindah dari laptop ke cloud tanpa refactor besar

### Perkiraan harga

Harga RunPod bersifat dinamis tergantung GPU, region, dan tipe cloud.

Angka acuan resmi yang masih relevan dari domain RunPod:
- **RTX 4090 Community Cloud**: mulai sekitar **$0.44/jam**
- **RTX 4090 Secure Cloud**: mulai sekitar **$0.74/jam**
- **RTX A5000**: sekitar **$0.16-$0.29/jam** pada contoh resmi RunPod
- **Storage network volume**: mulai **$0.07/GB/bulan** untuk 1 TB pertama

### Cocok pilih GPU apa
- **RTX 4090 24 GB**: pilihan terbaik untuk skripsi Anda jika budget cukup
- **RTX A5000 / L4 / 3090**: lebih hemat, cocok untuk eksperimen menengah
- hindari GPU terlalu kecil jika ingin training semua kelas dengan setting lebih berat

### Cara implementasi ke aplikasi saat ini

#### Skenario yang disarankan
Pakai RunPod untuk **training**, lalu hasil model dibawa kembali ke repo lokal Anda.

#### Step-by-step
1. Pastikan repo Anda sudah terbaru di GitHub:
   `https://github.com/bagazsetyo/skripsi.git`
2. Siapkan dataset lokal agar mudah diupload:
   - folder yang dibutuhkan: `data/traffic_sign`
3. Buat akun RunPod dan isi credit secukupnya.
4. Buat `Pod` baru dengan template PyTorch atau CUDA/PyTorch yang mendukung Docker.
5. Pilih GPU:
   - minimal yang saya sarankan: `RTX 4090 24 GB`
   - opsi hemat: `A5000`, `L4`, atau `3090`
6. Tambahkan persistent storage jika ingin hasil training tidak hilang setelah pod dimatikan.
7. Masuk ke pod via terminal/Jupyter.
8. Clone repo:
   ```bash
   git clone https://github.com/bagazsetyo/skripsi.git
   cd skripsi
   ```
9. Upload dataset ke pod, lalu letakkan ke:
   ```text
   data/traffic_sign
   ```
10. Jalankan training.

    Opsi A, paling dekat dengan project saat ini:
    ```bash
    docker compose run --rm train
    ```

    Opsi B, jika ingin custom parameter:
    ```bash
    docker compose run --rm train python train.py --data-dir /app/data/traffic_sign --epochs 20 --batch-size 2 --image-size 512 --amp --model-name hustvl/yolos-tiny
    ```
11. Setelah training selesai, ambil hasil model dari:
    ```text
    backend/models/
    ```
12. Download hasil model ke lokal.
13. Letakkan hasil model ke folder lokal:
    ```text
    backend/models/
    ```
14. Jalankan backend lokal Anda, lalu aktifkan model dari halaman `Training & Model`.

### Kelebihan
- paling natural untuk stack sekarang
- mudah untuk training banyak model
- enak untuk eksperimen subset kelas vs semua kelas

### Kekurangan
- tetap perlu upload dataset manual
- harga final tergantung GPU yang tersedia saat itu
- perlu disiplin mematikan pod agar biaya tidak bocor

---

## 2. DigitalOcean Paperspace

### Kenapa cocok untuk project ini
- platform lebih “rapi” dan formal
- pricing GPU dipublikasikan jelas
- ada machine GPU yang cukup mudah dipakai untuk workflow Docker atau terminal biasa

### Harga resmi yang relevan

GPU machine resmi per jam:
- **A4000**: **$0.76/jam**
- **A5000**: **$1.38/jam**
- **A6000**: **$1.89/jam**
- **A100**: **$3.09/jam**

Storage block:
- **100 GB**: **$0.0104/jam**, maksimum **$7/bulan**

### GPU yang saya sarankan
- **A4000**: paling masuk akal untuk mulai
- **A5000**: lebih aman untuk training yang lebih berat
- **A6000**: bagus kalau ingin ruang VRAM lebih lega
- **A100**: terlalu mahal untuk kebutuhan skripsi biasa, kecuali benar-benar perlu

### Cara implementasi ke aplikasi saat ini

#### Skenario yang disarankan
Pakai Paperspace untuk **machine GPU sementara**, lalu training project seperti di lokal.

#### Step-by-step
1. Buat akun DigitalOcean/Paperspace.
2. Buat `GPU Machine`.
3. Pilih salah satu:
   - `A4000` untuk hemat
   - `A5000` untuk lebih aman
4. Pilih storage minimal `100 GB` jika dataset dan output model ingin lebih nyaman.
5. Masuk ke machine via SSH atau terminal web.
6. Install Docker dan Docker Compose jika template machine belum menyiapkannya.
7. Clone repo:
   ```bash
   git clone https://github.com/bagazsetyo/skripsi.git
   cd skripsi
   ```
8. Upload dataset ke:
   ```text
   data/traffic_sign
   ```
9. Jalankan training:
   ```bash
   docker compose run --rm train
   ```
10. Jika perlu tuning, jalankan ulang dengan parameter yang berbeda.
11. Setelah model selesai, download isi folder:
   ```text
   backend/models/
   ```
12. Salin hasil model ke lokal Anda agar bisa dipakai di backend lokal.

### Kelebihan
- harga jelas
- setup masih cukup masuk akal
- cocok untuk training model yang perlu durasi lebih stabil

### Kekurangan
- umumnya lebih mahal dari opsi paling hemat
- tetap perlu setup environment machine
- kurang fleksibel dibanding marketplace yang lebih murah

---

## Perbandingan Singkat

| Produk | Tingkat Setup | Harga Acuan | Cocok untuk Anda | Catatan |
|---|---|---:|---|---|
| RunPod | Sedang | RTX 4090 mulai sekitar $0.44-$0.74/jam | Sangat cocok | Rekomendasi utama |
| DigitalOcean Paperspace | Sedang | A4000 $0.76/jam, A5000 $1.38/jam, A6000 $1.89/jam | Cocok | Harga lebih jelas |

---

## Saran Praktis untuk Skripsi Ini

Kalau tujuan Anda adalah **menyelesaikan training model utama dan beberapa eksperimen** tanpa terlalu banyak membuang waktu setup:

1. Pakai **RunPod** untuk training utama.
2. Gunakan **RTX 4090** jika tersedia dan budget masih aman.
3. Simpan hasil model per eksperimen ke folder berbeda.
4. Download hanya model terbaik ke lokal.
5. Gunakan backend lokal + frontend lokal untuk demo, bukan jalankan full app terus di cloud.

Alasannya:
- biaya lebih hemat
- workflow tetap sederhana
- hasil akhir tetap cocok dengan arsitektur aplikasi Anda sekarang

---

## Workflow yang Paling Aman

### Pola kerja yang saya sarankan
1. Development aplikasi tetap di lokal.
2. Training berat dilakukan di cloud GPU.
3. Hasil model diunduh ke lokal.
4. Model dimasukkan ke `backend/models/`.
5. Model diaktifkan dari aplikasi lokal.
6. Demo skripsi tetap memakai laptop lokal agar lebih stabil.

---

## Sumber

- RunPod Pricing: https://www.runpod.io/pricing
- RunPod Docs Pricing: https://docs.runpod.io/pods/pricing
- RunPod RTX 4090 Guide: https://www.runpod.io/articles/guides/nvidia-rtx-4090
- RunPod RTX A5000 Guide: https://www.runpod.io/articles/guides/nvidia-rtx-a5000-gpu
- DigitalOcean Paperspace Pricing: https://docs.digitalocean.com/products/paperspace/pricing/
- DigitalOcean GPU Pricing: https://www.digitalocean.com/pricing/additional-gpus
