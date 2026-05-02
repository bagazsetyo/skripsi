# Perancangan UML (Penjelasan Detail)

## Alur Sistem (Training sampai Output Prediksi)
1. Admin menyiapkan dataset dari Kaggle dan memastikan struktur folder train/test sesuai kelas.
2. Sistem membaca dataset, melakukan preprocessing (resize/normalisasi), dan menyiapkan data untuk training.
3. Admin mengatur konfigurasi training (epochs, learning rate, batch size, model name).
4. Sistem menjalankan training YOLOS dan menyimpan model terbaik/terakhir.
5. Admin mengaktifkan model yang akan digunakan untuk prediksi.
6. User mengunggah gambar pada aplikasi web.
7. Backend melakukan inferensi menggunakan model YOLOS aktif.
8. Sistem mengembalikan output berupa bounding box, label kelas, dan confidence.

## Activity Diagram
Referensi file: `uml/Activity-Diagram.mmd`

### Alur Training
1. Actor: Admin memulai proses training.
2. Sistem memuat dataset dari Kaggle.
3. Sistem melakukan preprocessing dan membagi data train/val/test.
4. Sistem mengonfigurasi model YOLOS sesuai parameter training.
5. Sistem menjalankan training dan menghitung loss per epoch.
6. Sistem melakukan evaluasi metrik (IoU, precision, recall, mAP).
7. Sistem menyimpan model dan mencatat riwayat training.

### Alur Prediksi
1. Actor: User mengunggah gambar ke aplikasi.
2. Sistem melakukan preprocessing gambar.
3. Sistem menjalankan inferensi YOLOS.
4. Sistem melakukan postprocess (bbox, label, score).
5. Sistem menampilkan hasil deteksi kepada user.

## Use Case Diagram
Referensi file: `uml/Use-Case-Diagram.mmd`

### Actor: Admin
1. Scan Dataset: memeriksa struktur data dan jumlah sampel per kelas.
2. Pilih Kelas: menentukan kelas yang akan digunakan dalam training.
3. Train Model: memulai proses pelatihan dengan parameter tertentu.
4. Lihat History Training: memantau hasil dan metrik training sebelumnya.
5. Aktifkan Model: memilih model yang akan dipakai untuk inferensi.

### Actor: User
1. Upload Gambar: mengirim gambar ke sistem untuk diprediksi.
2. Lihat Hasil Deteksi: melihat bounding box, label, dan confidence.

## Sequence Diagram
Referensi file: `uml/Sequence-Diagram.mmd`

1. User mengunggah gambar melalui UI React.
2. React mengirim request ke FastAPI endpoint `/predict`.
3. FastAPI meneruskan gambar ke YOLOS untuk inferensi.
4. YOLOS mengembalikan hasil prediksi (bbox, label, score).
5. FastAPI mengembalikan hasil ke UI React.
6. React menampilkan hasil deteksi ke user.
7. (Opsional) FastAPI menyimpan log prediksi ke SQLite.
