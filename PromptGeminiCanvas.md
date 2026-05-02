# Prompt Gemini Canvas (UI Layout)

Buat layout UI web yang sederhana untuk sistem deteksi rambu lalu lintas berbasis Vision Transformer. Fokus hanya pada 1–3 halaman berikut (jangan tambahkan halaman lain):

1) Dashboard/Overview
- Ringkasan proyek: jumlah kelas, jumlah data train/test, status model aktif.
- Kartu metrik terakhir (loss, mAP, precision, recall) dengan placeholder nilai.
- Section status sistem: GPU/CPU, model path, timestamp training terakhir.

2) Training & Model Management
- Form sederhana untuk konfigurasi training (epochs, learning rate, batch size, model name).
- Tombol tindakan: Start Training, Stop, Save Model, Set Active Model.
- Table riwayat training (tanggal, hyperparameter ringkas, hasil mAP, status).

3) Dataset Explorer
- Statistik dataset per kelas (list atau bar chart placeholder).
- Preview grid beberapa gambar contoh per kelas (placeholder).
- Info format anotasi YOLO dan struktur folder data.

Ketentuan desain:
- Gunakan layout bersih dan minimal (tidak perlu animasi kompleks).
- Gunakan warna netral dengan 1 warna aksen.
- Komponen UI sederhana, jangan menambah fitur di luar scope.
- Jangan membuat halaman "Predict" (akan dibuat terpisah nanti).
- Tampilkan navigasi sederhana (sidebar atau topbar) yang mengarah ke 3 halaman di atas.

Output yang diinginkan:
- 1–3 layout wireframe/low-fidelity.
- Setiap layout jelaskan struktur komponen dan hierarki konten.
