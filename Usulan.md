# Usulan Tugas Akhir

## Judul
Implementasi Vision Transformer untuk Deteksi dan Klasifikasi Rambu Lalu Lintas Indonesia

## Latar Belakang Metode
Vision Transformer (ViT) diperkenalkan oleh Alexey Dosovitskiy dkk. melalui makalah "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale" (2020, dipublikasikan di ICLR 2021). ViT mengubah citra menjadi rangkaian patch, kemudian memprosesnya menggunakan arsitektur Transformer, sehingga pemodelan tidak bergantung pada operasi konvolusi seperti CNN.

Untuk deteksi objek, pendekatan transformer kemudian dikembangkan menjadi YOLOS (You Only Look at One Sequence, 2021) yang memanfaatkan ViT untuk tugas deteksi secara end-to-end. Metode ini memandang deteksi sebagai permasalahan pemrosesan urutan, sehingga dapat menggabungkan informasi global pada gambar dengan lebih baik.

Fungsi utama metode Vision Transformer dalam proyek ini adalah melakukan deteksi dan klasifikasi rambu lalu lintas secara akurat, dengan memanfaatkan pretrained model agar mampu bekerja pada dataset berukuran terbatas.

## Implementasi Pada Proyek Ini
Pada proyek ini, Vision Transformer digunakan untuk mendeteksi dan mengklasifikasikan rambu lalu lintas Indonesia. Model yang dipakai adalah YOLOS (varian tiny) sebagai detektor berbasis transformer.

Implementasi utama berada pada:
- `backend/train.py`: proses training YOLOS (`YolosForObjectDetection`).
- `backend/app/inference.py`: memuat model dan menjalankan prediksi.
- `backend/app/main.py`: API FastAPI untuk endpoint `/predict`.
- `backend/dataset.py`: pembacaan dataset dan konversi anotasi YOLO menjadi format COCO untuk YOLOS.

## Detail Training (Ringkas)
- Dataset: `data/traffic_sign` (train dan test) dengan anotasi format YOLO.
- Kelas: mengikuti `CLASS_NAMES` di `backend/config.py` dan dapat ditambah.
- Model: `hustvl/yolos-tiny` (pretrained).
- Epoch: 30 (default).
- Batch size: 2.
- Learning rate: 1e-4.
- Weight decay: 1e-4.
- Scheduler: StepLR (step 10, gamma 0.5).
- AMP: aktif untuk efisiensi GPU (opsional).
- Threshold prediksi: 0.5 (default, bisa diubah via `SCORE_THRESHOLD`).
- GPU: NVIDIA RTX 3050 4GB.
