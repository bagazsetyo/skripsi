# Panduan Jawab Pertanyaan Dosen — Skripsi Deteksi Rambu Lalu Lintas

Dokumen ini berisi pertanyaan-pertanyaan yang mungkin diajukan dosen beserta
jawaban yang siap dikutip. Dikelompokkan per topik.

---

## A. Arsitektur Model — Vision Transformer & YOLOS

---

**Q: Mengapa menggunakan Vision Transformer (YOLOS), bukan CNN seperti YOLOv5/YOLOv8?**

A: YOLOS dipilih karena:
1. **End-to-end detection tanpa anchor** — tidak memerlukan hyperparameter anchor
   yang perlu di-tuning manual per dataset
2. **Global context** — self-attention di ViT menangkap hubungan antar seluruh
   bagian gambar sekaligus, sedangkan CNN hanya melihat receptive field lokal
3. **Pretrained pada ImageNet** — backbone ViT-small sudah belajar representasi
   visual yang kaya, sehingga fine-tuning pada dataset rambu lebih efisien
4. **Relevansi riset terkini** — ViT-based detection adalah arah pengembangan
   model deteksi objek mutakhir (state-of-the-art)

---

**Q: Ada dosen yang bilang ViT terlalu sederhana, seperti CNN saja. Bagaimana merespons ini?**

A: Pernyataan ini perlu diluruskan secara teknis:
- CNN menggunakan **convolution kernel** yang hanya melihat area lokal (local
  receptive field). Untuk menangkap konteks global, CNN butuh banyak lapisan
  (depth) dan pooling.
- ViT menggunakan **self-attention** yang setiap patch langsung bisa "berkomunikasi"
  dengan semua patch lain dalam satu operasi — ini secara komputasi lebih kompleks
  (O(N²) terhadap jumlah patch, vs O(N) per layer untuk CNN).
- YOLOS khususnya mengadaptasi arsitektur **BERT** (model bahasa transformer) untuk
  deteksi objek — merupakan pendekatan yang non-trivial dan berbeda secara fundamental
  dari CNN.
- Kompleksitas bukan dari jumlah layer, tetapi dari **mekanisme attention multi-head**
  yang memproses semua patch secara paralel dengan bobot yang dipelajari.

Singkatnya: ViT lebih kompleks secara komputasi dan konseptual dibanding CNN standar,
hanya arsitekturnya berbeda paradigma.

---

**Q: Apa itu YOLOS? Apa bedanya dengan YOLO biasa?**

A:

| Aspek | YOLO (CNN-based) | YOLOS (ViT-based) |
|-------|-----------------|-----------------|
| Backbone | CNN (Darknet, CSP) | Vision Transformer (ViT) |
| Mekanisme | Convolution + Feature Pyramid | Multi-head Self-Attention |
| Anchor | Ya (anchor-based) | Tidak (anchor-free) |
| Detection head | Grid cell prediction | 100 detection tokens |
| Assignment | Grid assignment | Hungarian Matching |
| Pretrain | ImageNet (CNN style) | ImageNet (patch embedding) |

YOLOS = "You Only Look One-level Feature Sequences" — dikembangkan oleh Hu et al.
(2022), mengadaptasi arsitektur ViT-small untuk deteksi objek dengan cara menambahkan
**detection tokens** di atas sequence patch gambar, mirip seperti `[CLS]` token di BERT.

---

**Q: Apa itu Hungarian Matching Loss?**

A: Dalam arsitektur DETR/YOLOS, model selalu memprediksi tepat **100 bounding box**
setiap forward pass (dari 100 detection tokens). Masalahnya: ground truth bisa hanya
1-5 box. Bagaimana menentukan box mana yang "benar" dan mana yang "kosong"?

**Hungarian Algorithm** menyelesaikan ini sebagai masalah *assignment* optimal:
- Hitung biaya (cost) antara setiap prediksi dan setiap GT box
  (berdasarkan class probability + bbox L1 + bbox GIoU)
- Temukan pasangan satu-ke-satu yang meminimalkan total biaya
- Pasangan yang tidak cocok ke GT box → prediksi "no-object" (dikenai loss kecil)

Ini memastikan setiap GT box ditangani tepat oleh satu prediksi, tanpa NMS
(Non-Maximum Suppression) yang dibutuhkan CNN-based detector.

---

**Q: Apa itu patch embedding di ViT?**

A: Gambar input dibagi menjadi patch-patch berukuran 16×16 piksel. Setiap patch
di-flatten dan di-proyeksikan ke vektor embedding 384 dimensi (untuk ViT-small).
Patch-patch ini diperlakukan seperti kata-kata dalam kalimat — setiap patch adalah
satu "token". Untuk gambar 500×500, terbentuk ≈ 976 patch tokens; untuk 700×700,
≈ 1.914 patch tokens. Inilah mengapa image size yang lebih besar memperlambat
training secara kuadratik (O(N²) attention).

---

## B. Konfigurasi Training

---

**Q: Mengapa batch_size = 2?**

A: Batch size 2 digunakan karena GPU NVIDIA A100 (80 GB) memiliki VRAM yang cukup:
konsumsi terukur untuk img600 bs=2 adalah ~43 GB, jauh di bawah batas 80 GB.
Batch size 2 memberikan estimasi gradient yang lebih stabil dibanding bs=1,
sehingga konvergensi lebih mulus. Ketiga konfigurasi (img500/600/700) menggunakan
bs=2 yang sama untuk menjaga konsistensi perbandingan.

Untuk mengatasi potensi instabilitas gradient dengan bs=1, digunakan:
- **LR Warmup** — learning rate tidak langsung penuh di epoch pertama, naik
  bertahap selama 3 epoch agar bobot menyesuaikan sebelum update besar
- **Gradient Clipping (0.1)** — membatasi magnitude gradient agar tidak meledak
- **Cosine Decay** — LR turun halus ke akhir training, mengurangi osilasi

Dalam praktik, YOLOS dan DETR memang umumnya dilatih dengan batch size kecil
(1–4) karena ukuran model transformer yang besar.

---

**Q: Mengapa Learning Rate = 5×10⁻⁵?**

A: LR 5×10⁻⁵ (0.00005) adalah nilai yang umum digunakan untuk **fine-tuning**
model pretrained berbasis transformer. Alasan:
- LR terlalu besar (>1×10⁻⁴) dapat merusak bobot pretrained yang sudah baik
  (disebut "catastrophic forgetting")
- LR terlalu kecil (<1×10⁻⁵) membuat fine-tuning sangat lambat dan model bisa
  "terjebak" di representasi pretrained tanpa beradaptasi ke dataset baru
- 5×10⁻⁵ terbukti menghasilkan mAP@0.5 = 92.07% pada model img600, menunjukkan
  nilai ini tepat untuk dataset rambu lalu lintas Indonesia ini

---

**Q: Apa itu Cosine Decay dan LR Warmup? Kenapa tidak pakai LR tetap?**

A:
- **LR Warmup**: Di 3 epoch pertama, LR naik linear dari 0 → 3×10⁻⁵. Ini penting
  karena pada awal training, bobot model belum "siap" untuk update besar — warmup
  memberi waktu adaptasi dan menghindari divergensi di epoch awal.
- **Cosine Decay**: Setelah warmup, LR turun mengikuti kurva kosinus dari 3×10⁻⁵
  ke ≈ 1×10⁻⁶. Turunan yang halus (bukan step) membantu model fine-tuning di
  akhir training tanpa melompati minimum loss.
- **vs LR tetap**: LR tetap sering menyebabkan osilasi di sekitar minimum (tidak
  bisa "landing" halus). Scheduler yang baik umumnya menghasilkan model akhir
  yang lebih baik 1–3% mAP.

---

**Q: Mengapa menggunakan AdamW, bukan Adam atau SGD?**

A:
- **Adam vs AdamW**: AdamW memisahkan weight decay dari update gradient. Pada Adam
  biasa, weight decay terkait dengan skala gradient (sehingga tidak benar-benar
  L2 regularisasi). AdamW memperbaiki ini → regularisasi lebih efektif, umumnya
  menghasilkan generalisasi lebih baik.
- **SGD vs AdamW**: SGD butuh LR tuning yang lebih hati-hati dan biasanya
  membutuhkan lebih banyak epoch untuk konvergen. Untuk model transformer,
  AdamW adalah standar de-facto (digunakan di BERT, ViT, DETR, YOLOS semua).

---

**Q: Apa itu Gradient Clipping dan kenapa nilainya 0.1?**

A: Gradient clipping memotong magnitude gradient menjadi maksimal 0.1 sebelum
update bobot. Ini mencegah **exploding gradient** — fenomena di mana gradient
menjadi sangat besar (terutama di lapisan attention transformer) dan menyebabkan
update bobot yang tidak terkendali sehingga training diverge (loss meledak).
Nilai 0.1 adalah rekomendasi dari paper DETR/YOLOS original.

---

**Q: Apa itu Mixed Precision (AMP)?**

A: Automatic Mixed Precision (AMP) menjalankan sebagian operasi dalam presisi
FP16 (16-bit float) alih-alih FP32 (32-bit). Manfaat:
- **VRAM lebih hemat** (~50% untuk aktivasi) → bisa melatih model lebih besar
- **Komputasi lebih cepat** (~2× pada GPU modern yang mendukung Tensor Core)
- Akumulasi gradient tetap FP32 untuk menjaga numerik stabil

AMP aman digunakan dengan gradient clipping dan loss scaling otomatis.

---

**Q: Apa itu Weight Decay = 1×10⁻⁴?**

A: Weight decay adalah regularisasi L2 — setiap update bobot dikurangi sedikit
(1×10⁻⁴ × nilai bobot). Efeknya: bobot tidak tumbuh terlalu besar, model
dipaksa menggunakan banyak bobot kecil daripada beberapa bobot sangat besar.
Ini mencegah overfitting, terutama penting pada dataset berukuran sedang (~6.000
gambar) yang lebih mudah dihafal model dibanding dataset besar (jutaan gambar).

---

**Q: Mengapa epochs untuk img700 hanya 30, sedangkan img500 dan img600 = 40?**

A: Setiap epoch img700 memakan waktu ~1.85× lebih lama dari img600 karena jumlah
patch ViT yang lebih banyak (~1.914 patch vs ~1.406 patch di img600). Self-attention
berskala O(N²) terhadap jumlah patch, sehingga img700 secara signifikan lebih lambat.
Dengan 40 epoch, img700 akan memakan ~16 jam di A100 — terlalu lama. Dengan 30 epoch
(~12 jam), total gradient steps tetap sebanding:
- img500: 40 × (5494/2) = 109.880 steps
- img600: 40 × (5494/2) = 109.880 steps
- img700: 30 × (5494/2) = 82.410 steps

Selisih ~25% steps untuk img700 dianggap wajar mengingat efisiensi komputasi.

---

## C. Dataset & Pembagian Data

---

**Q: Darimana data training diperoleh?**

A: Data berasal dari dua sumber:
1. **Dataset publik (Roboflow Universe)** — beberapa arsip dataset rambu lalu
   lintas Indonesia yang tersedia bebas, dipilih yang relevan dengan 18 kelas
   target penelitian
2. **Anotasi mandiri** — gambar tambahan yang dikumpulkan dan dianotasi secara
   manual menggunakan alat anotasi yang dikembangkan sebagai bagian dari sistem ini

Semua data disimpan dalam format YOLO (`class_id cx cy w h` normalized).

---

**Q: Kenapa rasio train:test = 91:9, bukan 80:20 seperti yang umum?**

A: Rasio 91:9 merupakan **konsekuensi dari metode stratified sampling dengan
fixed test size**, bukan keputusan acak.

Cara pembagiannya:
- Test set ditetapkan **30 gambar per kelas × 18 kelas = 540 gambar** (tetap)
- Seluruh data sisanya menjadi train
- Seiring penambahan data train, persentase test otomatis turun ke ~9%

Justifikasi: Dalam riset deteksi objek multi-kelas, ukuran test set yang seragam
per kelas lebih penting dari persentasenya. Dengan 30 sampel per kelas, evaluasi
tetap representatif untuk semua 18 kelas. Pendekatan serupa digunakan di benchmark
PASCAL VOC yang menjaga test set tetap untuk konsistensi evaluasi lintas eksperimen.

---

**Q: Apa itu Stratified Sampling?**

A: Stratified Sampling adalah metode pembagian data yang memastikan setiap kelas
terwakili secara proporsional di setiap split. Dibanding random sampling biasa:
- **Random**: bisa terjadi kelas dengan data sedikit tidak muncul sama sekali
  di test set (terutama kelas dengan hanya 70 gambar)
- **Stratified**: setiap kelas pasti ada di test set dengan jumlah yang terkontrol
  (30 gambar/kelas)

Hasil: evaluasi yang adil dan dapat diperbandingkan antar kelas.

---

**Q: Bagaimana menangani ketidakseimbangan data (class imbalance)?**

A: Distribusi data train cukup seimbang: 213–343 gambar per kelas. Penanganannya:
1. **Augmentasi data** (ColorJitter, GaussianBlur, RandomGrayscale) — meningkatkan
   variasi visual sehingga setiap kelas memiliki representasi
   yang lebih beragam
2. **Evaluasi per kelas** — mAP per kelas dipantau untuk mengidentifikasi kelas
   yang perlu data tambahan
3. **Penambahan data manual** — kelas dengan data sedikit (seperti larangan-belok-kiri
   dan petunjuk-penyeberangan-pejalan-kaki) ditambahkan gambar dari sumber tambahan

---

**Q: Mengapa hanya 18 kelas, tidak lebih?**

A: 18 kelas dipilih berdasarkan:
1. **Ketersediaan data** — hanya 18 kelas yang memiliki data cukup (minimal 70
   gambar per kelas) untuk dapat dilatih secara wajar
2. **Relevansi praktis** — 18 kelas mencakup rambu yang paling umum ditemui di
   jalan raya Indonesia: larangan, peringatan, perintah, dan petunjuk
3. **Keterbatasan GPU** — semakin banyak kelas, semakin besar memori yang diperlukan
   untuk detection head

---

**Q: Mengapa lampu lalu lintas (merah/kuning/hijau) tidak dimasukkan?**

A: Lampu lalu lintas bukan termasuk **rambu lalu lintas** menurut definisi
Peraturan Menteri Perhubungan. Rambu lalu lintas adalah tanda yang dipasang di
tiang atau portal di pinggir/atas jalan, sedangkan lampu lalu lintas adalah
alat pemberi isyarat lalu lintas (APILL) yang beroperasi secara dinamis.

Penelitian ini berfokus pada **deteksi rambu lalu lintas statis**, sehingga
APILL berada di luar cakupan. Memasukkannya justru dapat membingungkan model
karena karakteristik visualnya sangat berbeda dari rambu konvensional.

---

## D. Evaluasi Model

---

**Q: Apa itu mAP@0.5? Mengapa ini yang digunakan sebagai metrik utama?**

A: **mAP = mean Average Precision** — rata-rata dari AP (Area Under Precision-Recall
Curve) di semua kelas.

`@0.5` berarti prediksi dianggap benar (True Positive) jika IoU antara bounding
box prediksi dan ground truth ≥ 0.5 (50% overlap).

Mengapa mAP:
- Mengukur kualitas deteksi secara menyeluruh: lokasi box (IoU) + klasifikasi kelas
- Tidak sensitif terhadap pilihan threshold confidence tertentu (berbeda dengan
  accuracy atau F1 yang bergantung pada threshold)
- Standar industri untuk benchmark deteksi objek (COCO, PASCAL VOC, dll.)

---

**Q: Apa itu IoU (Intersection over Union)?**

A: IoU mengukur seberapa banyak overlap antara bounding box prediksi dan ground truth:

```
IoU = Luas (Prediksi ∩ GT) / Luas (Prediksi ∪ GT)
```

- IoU = 1.0: prediksi persis sama dengan GT
- IoU = 0.5: 50% area overlap (batas minimum untuk dianggap TP di mAP@0.5)
- IoU = 0.0: tidak ada overlap sama sekali

---

**Q: Apa bedanya Precision dan Recall?**

A:
- **Precision** = TP / (TP + FP) — dari semua yang diprediksi sebagai rambu X,
  berapa persen yang benar? (mengukur ketelitian)
- **Recall** = TP / (TP + FN) — dari semua rambu X yang ada di gambar, berapa
  persen yang berhasil terdeteksi? (mengukur kelengkapan)

Trade-off: Menurunkan score threshold → Recall naik (lebih banyak terdeteksi)
tapi Precision turun (lebih banyak false positive). mAP mengukur keseimbangan
keduanya di seluruh kurva threshold.

---

**Q: Mengapa score threshold = 0.3?**

A: Score threshold 0.3 berarti hanya prediksi dengan confidence ≥ 30% yang
ditampilkan. Nilainya dipilih berdasarkan pertimbangan:
- Threshold terlalu tinggi (>0.7): banyak deteksi benar yang dibuang (recall rendah)
- Threshold terlalu rendah (<0.2): banyak false positive yang muncul
- 0.3 adalah nilai umum untuk deteksi objek dengan dataset berukuran sedang
  di mana model belum sepenuhnya yakin terhadap semua kelas

Nilai ini bisa disesuaikan saat deployment tergantung kebutuhan aplikasi.

---

## E. Perbandingan Model

---

**Q: Mengapa membandingkan image size 500, 600, 700 px?**

A: Berdasarkan saran dosen pembimbing untuk membandingkan beberapa konfigurasi
input agar ada data empiris. Image size dipilih sebagai variabel karena:
1. Secara teoritis, resolusi lebih tinggi → detail visual lebih kaya → akurasi
   lebih baik untuk kelas yang secara visual mirip
2. Tradeoff jelas: resolusi tinggi → VRAM lebih besar, training lebih lambat
3. Mudah dikontrol: satu variabel berubah, semua parameter lain tetap sama
   (batch_size=1, epochs=30/30/25, LR=3×10⁻⁵, dll.)

---

**Q: Bagaimana cara menginterpretasikan jika hasilnya semua hampir sama?**

A: Jika selisih mAP antar ketiga model < 2%, artinya:
- Perbedaan resolusi 500–700 px **tidak signifikan** untuk dataset rambu lalu lintas
  ini, kemungkinan karena rambu sudah cukup besar di gambar sehingga 500 px sudah
  representatif
- Kesimpulan: **img500 direkomendasikan** untuk deployment karena inference lebih
  cepat dan membutuhkan hardware lebih rendah dengan akurasi yang setara

Jika ada perbedaan signifikan (>3%):
- Identifikasi kelas mana yang paling diuntungkan oleh resolusi tinggi
  (biasanya kelas dengan detail kecil atau perbedaan visual halus)

---

**Q: Mengapa tidak membandingkan dengan YOLOv8 atau model CNN lainnya?**

A: Fokus penelitian ini adalah pada **konfigurasi dan optimasi model YOLOS**,
bukan perbandingan antar arsitektur yang berbeda. Membandingkan ViT dengan CNN
memerlukan analisis yang lebih mendalam dan berada di luar cakupan penelitian ini.
Penelitian ini berkontribusi pada studi penerapan Vision Transformer untuk deteksi
rambu lalu lintas Indonesia, yang merupakan topik yang relatif baru di domain ini.

> Catatan: Jika dosen meminta perbandingan dengan CNN, ini bisa menjadi saran
> penelitian lanjutan (future work) yang dicantumkan di bagian penutup skripsi.

---

## F. Aplikasi & Deployment

---

**Q: Apakah sistem ini bisa digunakan secara real-time (video)?**

A: Ya. Sistem sudah dilengkapi fitur video demo (endpoint `/video-demo`) yang
memproses stream video secara real-time menggunakan WebRTC/getUserMedia pada
browser. Model YOLOS-small pada CPU/GPU dapat berjalan pada 10–30 FPS tergantung
hardware, yang cukup untuk aplikasi kendaraan bergerak lambat. Untuk kendaraan
otonom kecepatan tinggi, diperlukan hardware GPU yang lebih kuat atau optimasi
model lebih lanjut (quantization, TensorRT).

---

**Q: Di mana model di-deploy? Bagaimana arsitektur sistemnya?**

A: Sistem terdiri dari:
- **Backend**: FastAPI (Python) — menyajikan API prediksi, manajemen model, dan
  halaman web tools
- **Model**: YOLOS-small yang diload ke memori saat startup
- **Interface**: Web browser untuk upload gambar/video, atau API untuk integrasi

Training dilakukan di cloud (Google Colab A100), model hasil training di-download
sebagai file `.zip` lalu di-import ke sistem lokal melalui endpoint `/models/import`.

---

**Q: Apa keterbatasan sistem ini?**

A:
1. **Kualitas gambar** — model dilatih pada gambar statis; performa menurun pada
   gambar buram, gelap, atau sangat jauh
2. **Kelas terbatas** — hanya 18 kelas rambu; rambu yang tidak termasuk dalam
   daftar tidak akan terdeteksi
3. **Ketidakseimbangan data** — beberapa kelas memiliki data latih sedikit (70
   gambar) sehingga performa di kelas tersebut lebih rendah
4. **Hardware** — YOLOS-small relatif berat (>100M parameter); inferensi optimal
   memerlukan GPU, meski tetap bisa berjalan di CPU dengan kecepatan lebih lambat

---

## G. Pertanyaan Tentang Proses Penelitian

---

**Q: Bagaimana proses anotasi data dilakukan?**

A: Anotasi dilakukan menggunakan alat anotasi berbasis web yang dikembangkan
sendiri sebagai bagian dari sistem. Fitur:
- Upload gambar → gambar langsung ditampilkan
- Gambar bounding box dengan mouse (drag to draw)
- Pilih kelas dan split (train/test)
- Simpan → gambar + label YOLO otomatis tersimpan ke folder dataset

Selain itu, tersedia fitur import batch dari dataset publik yang sudah memiliki
anotasi, di mana pengguna memilih gambar yang relevan lalu memindahkannya ke
dataset dengan class label yang sesuai.

---

**Q: Bagaimana menjamin kualitas anotasi?**

A: Anotasi dari dataset publik (Roboflow) telah melalui proses kurasi komunitas.
Untuk anotasi mandiri, dilakukan verifikasi visual menggunakan endpoint `/annotate`
yang menampilkan bounding box di atas gambar sebelum disimpan. Dataset juga
diperiksa melalui endpoint `/dataset/validation` yang mendeteksi label yang hilang,
class ID yang tidak valid, dan format yang tidak sesuai.
