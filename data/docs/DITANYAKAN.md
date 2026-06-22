Berikut panduan untuk bimbingan besok:

---
Yang Perlu Disampaikan ke Dosen

1. Semua training sudah selesai
Ketiga model sudah selesai dilatih — img500, img600, img700 — dengan konfigurasi yang identik ning rate yang sama). Perbandingannya fair.

2. Batas atas image size di 700px
Di atas 700px rawan OOM karena VRAM sudah ~46–50 GB dari kapasitas 80 GB A100. Kalau dipaksa kiturunkan ke 1 sehingga kondisi training tidak lagi sama dan perbandingan jadi tidak fair.

3. Hasil: img600 terbaik
- img500: mAP 90.27%
- img600: mAP 92.07% ← terbaik
- img700: mAP 90.83%

Resolusi lebih tinggi tidak selalu lebih baik — img700 justru kalah dari img600.

4. Lampu lalu lintas tidak dimasukkan
Lampu lalu lintas (merah/kuning/hijau) dikeluarkan dari dataset karena bukan rambu lalu lintas (traffic sign), melainkan alat pemberi isyarat (traffic light) — kategori yang berbeda secara regulasi lalu lintas.
Penelitian ini fokus pada rambu, bukan sinyal.

---
Yang Perlu Ditanyakan ke Dosen

Terkait hasil:
- Kelas larangan-memutar-balik konsisten rendah di semua model (48–66%). Apakah ini cukup dicarlu penanganan khusus (tambah data, augmentasi lebih agresif)?

Terkait penulisan Bab 4:
- Apakah confusion matrix perlu ditampilkan secara visual (gambar/heatmap), atau cukup data nu
- Untuk kesimpulan model terbaik, apakah cukup berdasarkan mAP saja, atau perlu mempertimbangkan juga kecepatan inferensi?

Terkait dataset:
- Apakah rasio train:test 91:9 (stratified, 30 gambar per kelas di test) sudah dianggap cukup, atau ada saran perubahan?

Terkait scope:
- Apakah 18 kelas aktif sudah dianggap representatif, atau ada saran kelas tambahan yang perlu dipertimbangkan ke depannya?