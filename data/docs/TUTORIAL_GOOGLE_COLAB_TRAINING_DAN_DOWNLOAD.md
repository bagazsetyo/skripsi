# Tutorial Training Model di Google Colab dan Download ke Lokal

Dokumen ini berisi langkah praktis untuk:
- melakukan training model YOLOS di Google Colab
- menyimpan hasil training
- mendownload model ke komputer lokal
- memakai model hasil Colab pada aplikasi lokal

Tutorial ini disesuaikan dengan kondisi repo saat ini:
- source code ada di GitHub
- dataset **tidak** ada di GitHub
- model hasil training juga **tidak** ada di GitHub

## 1. Persiapan Sebelum Membuka Google Colab

Siapkan dulu di komputer lokal:

1. repo project ini
2. dataset yang akan dipakai untuk training
3. akun Google yang punya akses ke Google Drive

Saran:
- simpan dataset dalam bentuk folder `traffic_sign`
- atau zip dataset menjadi `traffic_sign.zip`

Struktur dataset yang diharapkan:

```text
traffic_sign/
  train/
    <nama_kelas>/
      *.jpg
      *.txt
  test/
    <nama_kelas>/
      *.jpg
      *.txt
```

Kalau nanti Anda sudah memakai split baru 80:20, pastikan struktur akhirnya tetap seperti di atas.

## 2. Cara Paling Aman Menyimpan Data di Colab

Yang paling disarankan:
- source code diambil dari GitHub
- dataset disimpan di Google Drive
- hasil model juga disimpan di Google Drive

Keuntungannya:
- kalau sesi Colab putus, file tetap aman
- model tidak hilang
- lebih mudah download ke lokal setelah training selesai

## 3. Buka Google Colab dan Aktifkan GPU

Langkah:
https://www.youtube.com/watch?v=P9kX9bdZzkQ

1. buka Google Colab
2. pilih `Runtime`
3. pilih `Change runtime type`
4. pada `Hardware accelerator`, pilih `GPU`
5. klik `Save`

Lalu cek GPU dengan cell ini:

```python
!nvidia-smi
```

## 4. Mount Google Drive

Jalankan cell berikut:
https://www.youtube.com/watch?v=JfrS9eGjLQU

```python
from google.colab import drive
drive.mount('/content/drive')
```

Setelah itu akan muncul link autentikasi. Ikuti prosesnya sampai Google Drive berhasil ter-mount.

## 5. Clone Repo ke Colab

Jalankan:

```python
%cd /content
!git clone https://github.com/bagazsetyo/skripsi.git
%cd /content/skripsi
```

## 6. Install Dependency

Jalankan:

```python
!pip install -r backend/requirements.txt
```

Catatan:
- `opencv-python` ikut ter-install, meskipun tidak wajib untuk training
- proses ini bisa memakan waktu beberapa menit

## 7. Siapkan Dataset di Colab

Karena folder `data/` tidak ada di GitHub, dataset harus dibawa sendiri.

Ada 2 cara.

### Opsi A - Dataset sudah ada di Google Drive

Misalnya Anda menyimpan dataset di:

```text
MyDrive/skripsi-data/traffic_sign
```

Maka jalankan:

```python
!mkdir -p /content/skripsi/data
!cp -r "/content/drive/MyDrive/skripsi-data/traffic_sign" "/content/skripsi/data/traffic_sign"
```

### Opsi B - Dataset dalam file zip di Google Drive

Misalnya file zip ada di:

```text
MyDrive/skripsi-data/traffic_sign.zip
```

Jalankan:

```python
!mkdir -p /content/skripsi/data
!unzip -q "/content/drive/MyDrive/skripsi-data/traffic_sign.zip" -d /content/skripsi/data
```

Setelah itu cek strukturnya:

```python
!ls /content/skripsi/data
!ls /content/skripsi/data/traffic_sign
```

## 8. Jalankan Training

Masuk ke folder backend:

```python
%cd /content/skripsi/backend
```

## 8A. Opsi yang paling disarankan: pakai runner otomatis

Repo ini sekarang sudah punya runner Colab otomatis di folder `colab/`, jadi Anda tidak perlu menulis command training panjang setiap kali eksperimen.

Contoh menjalankan preset `image size 500`:

```python
%cd /content/skripsi
!python colab/run_image_500.py --dataset-source "/content/drive/MyDrive/skripsi-data/traffic_sign.zip"
```

Contoh preset `image size 600`:

```python
%cd /content/skripsi
!python colab/run_image_600.py --dataset-source "/content/drive/MyDrive/skripsi-data/traffic_sign.zip"
```

Contoh preset `image size 700`:

```python
%cd /content/skripsi
!python colab/run_image_700.py --dataset-source "/content/drive/MyDrive/skripsi-data/traffic_sign.zip"
```

Runner tersebut akan otomatis:
- mount Google Drive jika perlu
- install dependency
- copy atau unzip dataset ke folder lokal repo
- menjalankan training
- menjalankan evaluasi
- menyimpan model
- menyimpan `metrics.json`
- menyimpan `training_summary.json`
- menyimpan `preset_config.json`

Output default akan tersimpan di:

```text
/content/drive/MyDrive/skripsi-models/
```

Catatan:
- Anda tetap bisa mengganti lokasi dataset dengan `--dataset-source`
- Anda juga bisa mengganti folder output dengan `--drive-output-root`
- jika dataset lokal ingin di-copy ulang, tambahkan `--force-dataset-copy`

## 8B. Opsi manual

Jika ingin tetap manual, gunakan command seperti di bawah.

Contoh training dasar:

```python
!python train.py \
  --data-dir /content/skripsi/data/traffic_sign \
  --epochs 30 \
  --batch-size 1 \
  --image-size 500 \
  --lr 0.00005 \
  --weight-decay 0.0001 \
  --amp \
  --output-dir /content/drive/MyDrive/skripsi-models/model-image-500
```

Contoh untuk perbandingan `image size`:

### Model 1 - Image Size 500

```python
!python train.py \
  --data-dir /content/skripsi/data/traffic_sign \
  --epochs 30 \
  --batch-size 1 \
  --image-size 500 \
  --lr 0.00005 \
  --weight-decay 0.0001 \
  --amp \
  --output-dir /content/drive/MyDrive/skripsi-models/model-image-500
```

### Model 2 - Image Size 600

```python
!python train.py \
  --data-dir /content/skripsi/data/traffic_sign \
  --epochs 30 \
  --batch-size 1 \
  --image-size 600 \
  --lr 0.00005 \
  --weight-decay 0.0001 \
  --amp \
  --output-dir /content/drive/MyDrive/skripsi-models/model-image-600
```

### Model 3 - Image Size 700

```python
!python train.py \
  --data-dir /content/skripsi/data/traffic_sign \
  --epochs 30 \
  --batch-size 1 \
  --image-size 700 \
  --lr 0.00005 \
  --weight-decay 0.0001 \
  --amp \
  --output-dir /content/drive/MyDrive/skripsi-models/model-image-700
```

## 9. Catat Hasil Training

Selama training, log yang tampil biasanya seperti:

```text
epoch=1 loss=...
epoch=2 loss=...
...
saved model to ...
```

Yang perlu Anda catat untuk Bab 4:
- nama model / nama run
- image size
- epochs
- batch size
- learning rate
- weight decay
- loss terakhir
- waktu training

Catatan:
- script `backend/train.py` saat ini menyimpan model dan processor
- evaluasi detail seperti `precision`, `recall`, `mAP`, dan `mean IoU` lebih lengkap tersedia di pipeline training web/backend
- jika Anda ingin evaluasi penuh dari Colab, nanti bisa dibuat tahap tambahan

## 10. Cek Hasil Model di Google Drive

Setelah training selesai, cek folder model:

```python
!ls "/content/drive/MyDrive/skripsi-models/model-image-500"
```

Biasanya akan muncul file seperti:
- `config.json`
- `preprocessor_config.json`
- `pytorch_model.bin`
- dan file model Hugging Face lain

## 11. Zip Model Sebelum Download

Agar mudah di-download, zip dulu folder model.

Contoh:

```python
%cd /content/drive/MyDrive/skripsi-models
!zip -r model-image-500.zip model-image-500
```

Kalau ingin zip model lain:

```python
!zip -r model-image-600.zip model-image-600
!zip -r model-image-700.zip model-image-700
```

## 12. Download Model ke Komputer Lokal

Ada 2 cara.

### Opsi A - Download langsung dari Google Drive

Setelah file zip ada di Google Drive:
- buka Google Drive
- masuk ke folder `skripsi-models`
- klik kanan file zip
- pilih `Download`

Ini cara paling mudah.

### Opsi B - Download langsung dari Colab

Jalankan:

```python
from google.colab import files
files.download('/content/drive/MyDrive/skripsi-models/model-image-500.zip')
```

Catatan:
- cara ini cocok untuk file yang tidak terlalu besar
- kalau file besar, kadang lebih stabil download dari Google Drive langsung

## 13. Cara Memakai Model Hasil Colab di Lokal

Saat ini fitur import model penuh di aplikasi belum final. Jadi cara paling mudah untuk sekarang adalah **manual**.

### Opsi paling mudah

1. ekstrak file zip hasil model
2. hasil ekstrak akan menjadi folder misalnya:

```text
model-image-500/
  config.json
  preprocessor_config.json
  pytorch_model.bin
  ...
```

3. copy folder itu ke:

```text
backend/models/
```

Sehingga menjadi:

```text
backend/models/model-image-500
```

### Agar langsung dipakai backend sekarang

Karena sistem saat ini paling mudah membaca model default dari:

```text
backend/models/yolos
```

maka cara tercepat adalah:

1. backup dulu folder:

```text
backend/models/yolos
```

2. ganti isinya dengan model hasil Colab

Atau:

1. rename model hasil Colab menjadi:

```text
backend/models/yolos
```

2. restart backend Docker:

```bash
docker compose up -d --build backend
```

Kalau container sudah mode volume mount dan dependency tidak berubah, biasanya cukup:

```bash
docker compose restart backend
```

Catatan penting:
- jika model baru memiliki konfigurasi kelas berbeda, pastikan class names tetap sesuai kebutuhan
- jika model dilatih untuk subset kelas, maka hasil deteksi hanya akan relevan untuk subset tersebut

## 14. Saran Penamaan Run Model

Agar rapi untuk Bab 4, gunakan nama seperti:

- `model-image-500`
- `model-image-600`
- `model-image-700`

Atau lebih lengkap:

- `yolos-img500-ep30-lr5e5`
- `yolos-img600-ep30-lr5e5`
- `yolos-img700-ep30-lr5e5`

Dengan begitu:
- lebih mudah dicatat di tabel Bab 4
- lebih mudah dibedakan saat download dan saat copy ke lokal

## 15. Ringkasan Alur Paling Praktis

Urutan paling ringkas:

1. buka Colab
2. aktifkan GPU
3. mount Google Drive
4. clone repo
5. install dependency
6. copy/unzip dataset ke `/content/skripsi/data/traffic_sign`
7. jalankan training
8. simpan output model ke Google Drive
9. zip model
10. download model ke lokal
11. copy model ke `backend/models/`
12. restart backend

## 16. Catatan Penting

- jika Colab putus di tengah jalan, file yang disimpan ke Google Drive tetap aman
- kalau training semua kelas terlalu berat, mulai dulu dari subset kecil untuk validasi
- untuk Bab 4, pastikan setiap eksperimen dicatat dengan konfigurasi yang jelas
- untuk pengujian utama, sebaiknya ubah **satu parameter utama saja**, yaitu `image size`

## 17. Contoh Checklist Sederhana

Checklist yang bisa Anda pakai:

- [ ] GPU Colab aktif
- [ ] Google Drive sudah di-mount
- [ ] Repo berhasil di-clone
- [ ] Dependency berhasil di-install
- [ ] Dataset berhasil dipindahkan ke Colab
- [ ] Training model image size 500 selesai
- [ ] Training model image size 600 selesai
- [ ] Training model image size 700 selesai
- [ ] Model sudah tersimpan di Google Drive
- [ ] Model sudah di-zip
- [ ] Model sudah di-download ke lokal
- [ ] Model sudah dicoba di aplikasi lokal
