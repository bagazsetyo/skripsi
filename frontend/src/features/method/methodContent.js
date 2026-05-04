import {
  AppstoreOutlined,
  BorderOutlined,
  CameraOutlined,
  NodeIndexOutlined,
  RadarChartOutlined,
  ScanOutlined,
} from "@ant-design/icons";

export const methodFlowSteps = [
  {
    key: "capture",
    title: "Gambar Dikirim ke Backend",
    icon: CameraOutlined,
    color: "green",
    summary:
      "Pengguna mengunggah satu gambar statis. Gambar ini dikirim dari frontend ke backend untuk diproses oleh model.",
    simple:
      "Ibaratnya, pengguna menyerahkan satu lembar foto ke sistem lalu sistem mulai memeriksanya.",
  },
  {
    key: "prepare",
    title: "Gambar Disiapkan",
    icon: ScanOutlined,
    color: "cyan",
    summary:
      "Backend menyesuaikan ukuran dan format gambar agar cocok dengan kebutuhan model YOLOS.",
    simple:
      "Sama seperti dokumen yang dirapikan dulu sebelum dibaca mesin, gambar juga disiapkan lebih dulu.",
  },
  {
    key: "patch",
    title: "Gambar Dibagi Menjadi Patch",
    icon: AppstoreOutlined,
    color: "purple",
    summary:
      "Gambar dipecah menjadi kotak-kotak kecil yang disebut patch. Setiap patch mewakili bagian kecil dari gambar.",
    simple:
      "Bayangkan gambar dipotong menjadi banyak ubin kecil agar mesin bisa memeriksa bagian demi bagian.",
  },
  {
    key: "token",
    title: "Patch Diubah Menjadi Token",
    icon: BorderOutlined,
    color: "gold",
    summary:
      "Setiap patch diterjemahkan menjadi representasi angka yang dapat dipahami model. Representasi ini biasa disebut token atau embedding.",
    simple:
      "Setelah gambar dipotong, tiap potongan diterjemahkan ke bahasa angka agar bisa dibaca komputer.",
  },
  {
    key: "attention",
    title: "Transformer Melihat Hubungan Antarbagian",
    icon: NodeIndexOutlined,
    color: "blue",
    summary:
      "Model transformer tidak hanya melihat satu patch sendirian. Model juga mempelajari hubungan antarpatch untuk memahami konteks gambar secara utuh.",
    simple:
      "Sistem tidak hanya melihat satu potongan, tetapi juga melihat bagaimana potongan-potongan itu saling berhubungan.",
  },
  {
    key: "detect",
    title: "Model Menentukan Lokasi dan Jenis Rambu",
    icon: RadarChartOutlined,
    color: "volcano",
    summary:
      "YOLOS memprediksi dua hal sekaligus: posisi objek dalam bentuk bounding box dan kelas objek, misalnya larangan parkir atau lampu merah.",
    simple:
      "Jadi model tidak hanya menjawab ‘ini rambu apa’, tetapi juga ‘rambunya ada di mana’.",
  },
];

export const analogies = [
  {
    title: "Analogi Puzzle",
    description:
      "Bayangkan sebuah foto dipecah menjadi banyak keping puzzle. Model tidak hanya mengenali satu keping, tetapi juga mempelajari hubungan antar keping untuk mengetahui gambar utuhnya.",
  },
  {
    title: "Analogi Membaca Peta",
    description:
      "Ketika melihat peta, kita tidak cukup hanya membaca satu titik. Kita juga memperhatikan jalan di sekitarnya. Transformer bekerja mirip seperti itu, yaitu melihat bagian dan konteksnya sekaligus.",
  },
  {
    title: "Analogi Pengawas Jalan",
    description:
      "Petugas di jalan tidak hanya melihat warna rambu, tetapi juga bentuk, posisi, dan lingkungan di sekitarnya. YOLOS mencoba meniru cara pandang seperti itu dalam bentuk model komputasi.",
  },
];

export const methodFacts = [
  {
    title: "Ini bukan klasifikasi gambar biasa",
    description:
      "Klasifikasi gambar biasa hanya menjawab isi gambar secara umum. YOLOS adalah object detection, sehingga keluaran model berupa letak objek dan jenis objek sekaligus.",
  },
  {
    title: "Kenapa cocok untuk rambu lalu lintas",
    description:
      "Rambu sering berukuran kecil dan muncul di latar yang ramai. Transformer membantu melihat hubungan antarbagian gambar sehingga konteks objek lebih mudah dipahami.",
  },
  {
    title: "Peran backend pada aplikasi ini",
    description:
      "Frontend hanya mengirim gambar dan menampilkan hasil. Proses utama seperti preprocessing, pemanggilan model, dan post-processing bounding box dilakukan di backend.",
  },
];

export const methodFaq = [
  {
    question: "Apakah YOLOS hanya menebak jenis rambu?",
    answer:
      "Tidak. YOLOS juga menentukan lokasi rambu dalam gambar. Karena itu hasilnya berupa bounding box dan label kelas.",
  },
  {
    question: "Apakah gambar benar-benar dipotong secara fisik?",
    answer:
      "Secara konsep iya, gambar dipandang sebagai patch-patch kecil. Namun prosesnya dilakukan sebagai representasi data untuk model, bukan seperti memotong file gambar manual satu per satu.",
  },
  {
    question: "Kenapa perlu preprocessing dulu?",
    answer:
      "Karena model membutuhkan ukuran dan format input yang konsisten. Tanpa itu, hasil prediksi bisa tidak stabil atau bahkan gagal diproses.",
  },
];
