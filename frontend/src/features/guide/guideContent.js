import {
  CameraOutlined,
  DashboardOutlined,
  DatabaseOutlined,
  RadarChartOutlined,
  RocketOutlined,
} from "@ant-design/icons";

export const quickStartSteps = [
  {
    title: "Cek Dataset",
    description:
      "Buka menu Dataset untuk melihat jumlah gambar, jumlah anotasi, dan memastikan data terbaca oleh sistem.",
  },
  {
    title: "Siapkan Training",
    description:
      "Masuk ke menu Training & Model untuk memilih semua kelas atau subset kelas, lalu jalankan training.",
  },
  {
    title: "Pilih Model Aktif",
    description:
      "Setelah model tersedia, aktifkan model yang ingin dipakai untuk proses prediksi.",
  },
  {
    title: "Jalankan Prediksi",
    description:
      "Buka menu Prediksi, unggah gambar rambu, lalu sistem akan menampilkan label, confidence, dan bounding box.",
  },
];

export const predictionTips = [
  "Gunakan gambar yang cukup jelas agar bentuk rambu mudah terbaca oleh model.",
  "Jika hasil deteksi terlalu sedikit, turunkan score threshold secara bertahap.",
  "Pastikan model aktif sudah sesuai dengan eksperimen yang ingin diuji.",
];

export const menuGuideDetails = [
  {
    key: "dashboard",
    title: "Dashboard",
    color: "geekblue",
    icon: DashboardOutlined,
    summary:
      "Menu ini menampilkan ringkasan umum sistem agar pengguna bisa langsung melihat kondisi aplikasi tanpa membuka semua halaman satu per satu.",
    imageLabel: "Placeholder Dashboard",
    description:
      "Dashboard cocok dipakai sebagai titik awal. Dari halaman ini pengguna dapat melihat model aktif, jumlah model yang tersedia, kondisi dataset, dan training run terbaru.",
    bullets: [
      "Gunakan dashboard untuk melihat kondisi umum sistem secara cepat.",
      "Bagian model aktif membantu memastikan prediksi memakai model yang benar.",
      "Riwayat training terbaru membantu melihat apakah ada eksperimen yang baru selesai atau gagal.",
    ],
    details: [
      {
        label: "Ringkasan Sistem",
        description:
          "Berisi kartu-kartu utama seperti jumlah kelas, jumlah model, training selesai, dan model aktif.",
      },
      {
        label: "Ringkasan Dataset",
        description:
          "Menunjukkan jumlah gambar dan anotasi agar kondisi data dapat dibaca tanpa masuk ke menu dataset.",
      },
      {
        label: "Training Terbaru",
        description:
          "Menampilkan run terakhir sehingga pengguna bisa melihat progres eksperimen dengan cepat.",
      },
    ],
  },
  {
    key: "dataset",
    title: "Dataset",
    color: "cyan",
    icon: DatabaseOutlined,
    summary:
      "Menu ini dipakai untuk membaca struktur data yang dipakai model, termasuk pembagian train-test, jumlah anotasi, dan validitas dataset.",
    imageLabel: "Placeholder Dataset",
    description:
      "Menu Dataset membantu memastikan data pelatihan memang siap digunakan. Halaman ini penting sebelum training dijalankan agar kesalahan data bisa diketahui lebih awal.",
    bullets: [
      "Lihat total gambar dan anotasi untuk mengetahui skala dataset.",
      "Periksa pembagian train dan test untuk memahami komposisi data.",
      "Gunakan hasil validasi untuk mendeteksi file label yang rusak atau tidak cocok.",
    ],
    details: [
      {
        label: "Refresh Dataset",
        description:
          "Tombol ini menjalankan pembaruan cache dataset di background. Digunakan saat isi folder dataset berubah dan ringkasannya perlu disegarkan.",
      },
      {
        label: "Summary Cards",
        description:
          "Menampilkan jumlah kelas, jumlah gambar, jumlah label, dan status validasi dataset secara singkat.",
      },
      {
        label: "Hasil Validasi Dataset",
        description:
          "Menunjukkan apakah dataset valid atau masih memiliki masalah seperti file label hilang, annotation format salah, atau class id tidak sesuai.",
      },
    ],
  },
  {
    key: "training",
    title: "Training & Model",
    color: "volcano",
    icon: RocketOutlined,
    summary:
      "Menu ini adalah pusat eksperimen model. Di sini pengguna membuat training run, memilih subset kelas, dan mengelola model yang tersedia.",
    imageLabel: "Placeholder Training & Model",
    description:
      "Halaman Training & Model dipakai terutama oleh admin. Bagian ini cukup penting karena banyak input yang memengaruhi hasil pelatihan model.",
    bullets: [
      "Buat training run baru sesuai eksperimen yang ingin dilakukan.",
      "Pilih apakah model dilatih dengan semua kelas atau hanya beberapa kelas tertentu.",
      "Aktifkan model yang dianggap paling baik untuk dipakai saat prediksi.",
    ],
    details: [
      {
        label: "Run Name",
        description:
          "Nama eksperimen training. Sebaiknya dibuat jelas agar mudah dibedakan dengan run lain.",
      },
      {
        label: "Selection Mode",
        description:
          "`All` berarti model dilatih dengan semua kelas yang tersedia. `Subset` berarti model hanya dilatih dengan kelas yang dipilih pengguna.",
      },
      {
        label: "Selected Classes",
        description:
          "Daftar kelas yang akan dipakai jika `Selection Mode` diatur ke `Subset`.",
      },
      {
        label: "Epochs",
        description:
          "Jumlah putaran training. Semakin besar nilainya, model belajar lebih lama, tetapi waktu training juga semakin panjang.",
      },
      {
        label: "Batch Size",
        description:
          "Jumlah gambar yang diproses setiap langkah training. Nilai besar biasanya butuh GPU lebih besar.",
      },
      {
        label: "Learning Rate",
        description:
          "Mengatur seberapa cepat model memperbarui bobotnya saat belajar. Nilai terlalu besar bisa membuat training tidak stabil.",
      },
      {
        label: "Score Threshold",
        description:
          "Nilai ambang yang dipakai saat evaluasi/prediksi untuk menentukan apakah suatu deteksi cukup yakin untuk ditampilkan.",
      },
      {
        label: "Activate After Training",
        description:
          "Jika aktif, model yang baru selesai training akan langsung dijadikan model aktif untuk prediksi.",
      },
      {
        label: "Daftar Model",
        description:
          "Menampilkan model yang tersedia dan menyediakan tombol untuk mengaktifkan model tertentu.",
      },
      {
        label: "Riwayat Training Run",
        description:
          "Menampilkan histori run sebelumnya agar eksperimen dapat dilacak dengan lebih rapi.",
      },
    ],
  },
  {
    key: "prediction",
    title: "Prediksi",
    color: "green",
    icon: RadarChartOutlined,
    summary:
      "Menu ini dipakai untuk menguji model dengan gambar statis dan melihat hasil deteksi rambu lalu lintas secara langsung.",
    imageLabel: "Placeholder Prediksi",
    description:
      "Halaman ini ditujukan untuk pengguna publik maupun admin. Alurnya dibuat sederhana agar orang yang tidak terbiasa dengan machine learning tetap bisa menggunakannya.",
    bullets: [
      "Unggah satu gambar statis.",
      "Atur threshold sesuai kebutuhan.",
      "Jalankan prediksi dan baca hasil bounding box, label, dan confidence.",
    ],
    details: [
      {
        label: "Model Aktif",
        description:
          "Menunjukkan model mana yang sedang dipakai backend untuk proses prediksi saat ini.",
      },
      {
        label: "Upload Gambar",
        description:
          "Area untuk memilih satu file gambar yang akan diprediksi.",
      },
      {
        label: "Score Threshold",
        description:
          "Semakin tinggi threshold, hasil yang muncul akan semakin selektif. Jika terlalu tinggi, beberapa objek bisa tidak tampil.",
      },
      {
        label: "Preview Hasil Prediksi",
        description:
          "Menampilkan gambar yang diunggah beserta bounding box hasil deteksi setelah prediksi berhasil dijalankan.",
      },
      {
        label: "Daftar Hasil Deteksi",
        description:
          "Menampilkan daftar objek yang terdeteksi lengkap dengan nama kelas dan nilai confidence.",
      },
    ],
  },
  {
    key: "camera",
    title: "Prediksi Dari Kamera",
    color: "purple",
    icon: CameraOutlined,
    summary:
      "Fitur ini direncanakan sebagai opsi ringan untuk mengambil foto dari kamera lalu mengirimkannya ke backend sebagai gambar statis.",
    imageLabel: "Placeholder Kamera",
    description:
      "Mode kamera tidak ditujukan untuk video real-time. Pendekatan yang dipilih adalah mengambil satu foto, lalu memprosesnya seperti gambar biasa.",
    bullets: [
      "Akses kamera dari browser.",
      "Ambil satu foto saat objek sudah terlihat jelas.",
      "Kirim foto ke backend dan tampilkan hasil seperti mode upload gambar.",
    ],
    details: [
      {
        label: "Kenapa bukan video real-time",
        description:
          "Video real-time lebih berat, lebih rumit, dan tidak diperlukan untuk scope skripsi yang berfokus pada gambar statis.",
      },
      {
        label: "Keuntungan mode kamera",
        description:
          "Lebih praktis untuk demo karena pengguna tidak perlu menyiapkan file gambar terlebih dahulu.",
      },
    ],
  },
];
