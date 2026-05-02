# Skripsi

Repositori ini digunakan untuk pengembangan aplikasi skripsi berjudul **Deteksi dan Klasifikasi Rambu Lalu Lintas Indonesia Menggunakan Vision Transformer**.

## Isi Repo

- `backend/`: backend FastAPI, training script, dataset loader, dan inference model
- `uml/`: diagram UML dan artefak perancangan
- `TODO.md`: breakdown task implementasi aplikasi
- `skirpsi.md`: draft isi skripsi / perancangan
- `text.txt`: draft wireframe / mockup UI

## Yang Tidak Di-push ke GitHub

Folder berikut sengaja **tidak** di-push karena ukurannya besar atau merupakan artefak lokal:

- `data/`
- `backend/models/`

Setelah clone repo ini, siapkan kembali:

1. Dataset di `data/traffic_sign`
2. Model hasil training di `backend/models/`

## Catatan Penting

- Dataset saat ini menggunakan 21 kelas rambu lalu lintas Indonesia
- Model hasil training dapat memiliki banyak versi
- Nanti aplikasi akan mendukung:
  - training semua kelas
  - training subset kelas tertentu
  - pemilihan model aktif untuk prediksi

## Menjalankan Backend

Lihat panduan pada [backend/README.md](/D:/Code/UP-V4/backend/README.md).

Secara umum:

```bash
docker compose up backend
```

Mode backend sekarang berjalan dalam mode development:
- source code `backend/` di-mount langsung ke container
- `uvicorn` dijalankan dengan `--reload`
- perubahan file Python tidak perlu rebuild image

Rebuild backend hanya diperlukan jika:
- `backend/requirements.txt` berubah
- `backend/Dockerfile` berubah
- base image/dependency container berubah

Untuk training:

```bash
docker compose --profile train up train
```

## Menjalankan Frontend

Frontend juga sudah disiapkan dalam mode development via Docker.

Jalankan:

```bash
docker compose up frontend
```

Atau jalankan backend dan frontend sekaligus:

```bash
docker compose up backend frontend
```

Mode frontend sekarang berjalan dalam mode development:
- source code `frontend/` di-mount langsung ke container
- Vite berjalan di `0.0.0.0:5173`
- perubahan file frontend tidak perlu rebuild image

Rebuild frontend hanya diperlukan jika:
- `frontend/package.json` berubah
- `frontend/Dockerfile` berubah
- dependency Node berubah

## Catatan Repo

- `docker-compose.yml` masih perlu dirapikan sebelum implementasi final
- `backend/config.py` masih perlu disinkronkan dengan 21 kelas final
- Frontend akan dibuat pada folder `frontend/`
