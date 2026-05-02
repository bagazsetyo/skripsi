BAB III
PERANCANGAN

3.1  Metode Penelitian
3.1.1 Teknik Pengumpulan Data
Teknik pengumpulan data pada penelitian ini menggunakan tiga pendekatan utama yang bertujuan untuk memperoleh data yang akurat dan relevan guna mengembangkan model deteksi dan klasifikasi rambu lalu lintas Indonesia menggunakan Vision Transformer (ViT).
1.	Akuisisi Dataset Publik
Dataset dikumpulkan melalui platform Kaggle yang menyediakan dataset rambu lalu lintas Indonesia dalam format citra digital dan anotasi. Proses akuisisi dilakukan dengan mengunduh dataset, memeriksa lisensi penggunaan, serta memvalidasi struktur data yang mencakup jumlah kelas, jumlah gambar, dan format anotasi bounding box. Dataset publik dipilih karena telah memiliki label terstandarisasi sehingga dapat digunakan langsung untuk proses pelatihan dan evaluasi model deteksi objek.
2.	Kurasi dan Validasi Data
Setelah dataset diperoleh, dilakukan kurasi untuk memastikan kualitas data dan kesesuaian anotasi. Tahap ini meliputi pengecekan konsistensi label kelas, validitas koordinat bounding box, keberadaan file yang rusak/duplikat, serta keseragaman format anotasi. Data yang tidak memenuhi kriteria kualitas dipisahkan agar tidak mengganggu proses pelatihan.
3.1.2 Model Pengembangan Sistem
Model pengembangan sistem ini terdiri dari dua bagian utama, yaitu pengembangan model (YOLOS/ViT) dan pengembangan perangkat lunak (backend–frontend), yang dirancang untuk sebagai prototipe sistem deteksi dan klasifikasi rambu lalu lintas berbasis unggah gambar.
1.	Persiapan Data & Konversi Anotasi
Dataset pada penelitian ini diperoleh dari Kaggle dan disusun dalam struktur folder train dan test, di mana setiap kelas rambu ditempatkan pada folder tersendiri. Setiap file gambar berformat .jpg memiliki pasangan file anotasi .txt dengan format YOLO, yaitu class_id x_center y_center width height dalam nilai ter-normalisasi. Satu file anotasi dapat memuat satu atau lebih baris anotasi apabila dalam satu gambar terdapat lebih dari satu rambu. Pada tahap persiapan data dilakukan pemeriksaan kesesuaian pasangan gambar–label, validasi format anotasi, serta proses pembacaan (parsing) anotasi untuk membentuk struktur target bounding box yang kompatibel dengan pipeline pelatihan model YOLOS/ViT.
2.	Pengembangan Model
Pengembangan model dilakukan menggunakan pendekatan Vision Transformer dengan model YOLOS untuk tugas deteksi dan klasifikasi rambu lalu lintas. Proses pelatihan memanfaatkan data pada subset train untuk menghasilkan model yang mampu memprediksi lokasi objek (bounding box) beserta label kelas dan confidence score. Model hasil pelatihan kemudian disimpan pada direktori backend/models dengan penamaan berbasis versi (misalnya models-v1, models-v2) agar proses eksperimen dan pergantian model dapat dilakukan dengan lebih terkontrol. Informasi model seperti versi, lokasi penyimpanan, dan status model aktif dicatat pada SQLite sehingga sistem prediksi selalu menggunakan model yang sedang ditetapkan sebagai model aktif.
3.2 Gambaran Umum Sistem 
Sistem yang dirancang pada penelitian ini merupakan prototipe aplikasi berbasis web untuk mendukung proses training model dan prediksi deteksi rambu lalu lintas Indonesia menggunakan pendekatan Vision Transformer, yaitu YOLOS. Sistem dijalankan pada lingkungan lokal menggunakan Docker agar dependensi dan konfigurasi lingkungan tetap konsisten. Secara umum, sistem terdiri dari tiga komponen utama, yaitu frontend (React) sebagai antarmuka pengguna, backend (FastAPI) sebagai layanan pemrosesan dan penghubung ke model, serta SQLite sebagai penyimpanan metadata model dan status model aktif.
Alur kerja sistem dibagi menjadi dua proses utama. Pertama adalah proses training, di mana admin mengakses halaman training untuk menjalankan pelatihan model berdasarkan dataset yang tersedia. Backend akan memuat data latih, membaca anotasi bounding box berformat YOLO, dan melakukan pelatihan model YOLOS sesuai konfigurasi yang ditentukan. Setelah training selesai, model disimpan ke folder backend/models dalam bentuk versi tertentu agar hasil eksperimen dapat dikelola dan digunakan kembali. Metadata mengenai versi model, lokasi penyimpanan, dan status model aktif kemudian dicatat pada SQLite. Alur proses training model pada sisi admin ditunjukkan pada Gambar 3.1. 
 
Gambar 3.1 Training Model

Proses kedua adalah prediksi, di mana pengguna mengunggah gambar statis melalui halaman prediksi. Backend akan memuat model yang sedang aktif berdasarkan informasi pada SQLite, melakukan prapemrosesan gambar, menjalankan inferensi menggunakan YOLOS, lalu mengembalikan keluaran prediksi berupa bounding box, label kelas, dan confidence score. Frontend menampilkan hasil tersebut dalam bentuk visualisasi sehingga pengguna dapat melihat hasil deteksi secara langsung setelah gambar diunggah. Alur proses prediksi rambu pada sisi pengguna ditunjukkan pada Gambar 3.2.
 
Gambar 3.2 Prediksi Gambar

3.3 Data Penelitian 
Data yang digunakan dalam penelitian ini berupa dataset rambu lalu lintas Indonesia yang diperoleh dari Kaggle [18]. Dataset disusun ke dalam dua subset, yaitu train dan test, dengan struktur direktori berbasis kelas. Setiap kelas rambu ditempatkan pada folder tersendiri dan berisi pasangan file gambar (.jpg) serta anotasi (.txt). Struktur ini dipilih karena sesuai untuk kebutuhan deteksi objek, yaitu menyediakan informasi kelas dan lokasi objek dalam citra. Contoh isi file anotasi ditunjukkan pada Tabel 3.3.
Setiap file anotasi menggunakan format YOLO, di mana satu baris anotasi merepresentasikan satu objek rambu pada gambar. Satu file .txt dapat berisi satu atau lebih baris apabila pada gambar terdapat lebih dari satu rambu. Format setiap baris anotasi adalah class_id x_center y_center width height, dengan class_id sebagai indeks kelas dan empat nilai lainnya sebagai koordinat bounding box dalam format titik tengah dan ukuran kotak dengan nilai ternormalisasi. Dengan format ini, dataset dapat digunakan untuk melatih model YOLOS agar menghasilkan prediksi berupa bounding box dan label kelas.
Secara implementasi, dataset berada pada direktori data/traffic_sign yang di dalamnya terdapat folder train dan test. Masing-masing subset memiliki daftar folder kelas yang sama, dan setiap file gambar memiliki file label dengan nama yang berpasangan. Ringkasan pemetaan kelas dan struktur dataset ditunjukkan pada Tabel 3.1 dan Tabel 3.2.
Tabel 3.1 Mapping Kelas
Class id	Nama Kelas	Direktori
0	Larangan Berhenti	larangan-berhenti
1	Larangan Masuk Bagi Kendaraan Bermotor dan Tidak Bermotor	larangan-masuk-bagi-kendaraan-bermotor-dan-tidak-bermotor
2	Larangan Parkir	larangan-parkir
3	Lampu Hijau	lampu-hijau
4	Lampu Kuning	lampu-kuning
5	Lampu Merah	lampu-merah
6	Larangan Belok Kanan	larangan-belok-kanan
7	Larangan Belok Kiri		larangan-belok-kiri
8	Larangan Berjalan Terus Wajib Berhenti Sesaat	larangan-berjalan-terus-wajib-berhenti-sesaat
9	Larangan Memutar Balik	larangan-memutar-balik
10	Peringatan Alat Pemberi Isyarat Lalu Lintas	peringatan-alat-pemberi-isyarat-lalu-lintas
11	Peringatan Banyak Pejalan Kaki Menggunakan Zebra Cross	peringatan-banyak-pejalan-kaki-menggunakan-zebra-cross
12	Peringatan Pintu Perlintasan Kereta Api	peringatan-pintu-perlintasan-kereta-api
13	Peringatan Simpang Tiga Sisi Kiri	peringatan-simpang-tiga-sisi-kiri
14	Peringatan Penegasan Rambu Tambahan	peringatan-penegasan-rambu-tambahan
15	Perintah Masuk Jalur Kiri	perintah-masuk-jalur-kiri
16	Perintah Pilihan Memasuki Salah Satu Jalur	perintah-pilihan-memasuki-salah-satu-jalur
17	Petunjuk Area Parkir	petunjuk-area-parkir
18	Petunjuk Lokasi Pemberhentian Bus	petunjuk-lokasi-pemberhentian-bus
19	Petunjuk Lokasi Putar Balik	petunjuk-lokasi-putar-balik
20	Petunjuk Penyeberangan Pejalan Kaki	petunjuk-penyeberangan-pejalan-kaki

Tabel 3.2 Struktur Dataset
Subset	Lokasi	Isi Utama
train	data/traffic_sign/train/<nama_kelas>/	.jpg, .txt
test	data/traffic_sign/test/<nama_kelas>/	.jpg, .txt


Tabel 3.3 Data Anotasi
Nama Kelas	File anotasi	Baris anotasi YOLO
Larangan Belok Kanan	larangan belok kanan (1).txt	6 0.514844 0.354911 0.182812 0.321429
Larangan Memutar Balik	larangan memutar balik (1).txt	9 0.464401 0.492933 0.404531 0.484099
Larangan Belok Kiri	larangan belok kiri (1).txt		7 0.301429 0.388041 0.074286 0.139949
Larangan Parkir	larangan parkir (1).txt	2 0.517595 0.335069 0.131965 0.156250
Larangan Masuk Bagi Kendaraan Bermotor dan Tidak Bermotor	larangan masuk bagi kendaraan bermotor dan tidak bermotor (1).txt	1 0.419935 0.417939 0.369281 0.522901

3.4 Perancangan Metode 
Perancangan metode pada penelitian ini disusun untuk mengimplementasikan proses deteksi dan klasifikasi rambu lalu lintas berbasis Vision Transformer menggunakan model YOLOS. Metode dirancang sebagai sebuah pipeline yang mencakup tahapan persiapan data, pembentukan target anotasi, pelatihan model, penyimpanan model hasil pelatihan, serta penggunaan model untuk proses prediksi pada gambar statis. Perancangan ini selaras dengan struktur dataset yang tersedia (train dan test) serta kebutuhan sistem prototipe yang menyediakan fitur training dan prediksi berbasis web.
Tahap awal pipeline adalah pembacaan dataset dari direktori data/traffic_sign dengan struktur folder per kelas. Pada tahap ini, sistem memetakan nama folder kelas menjadi identitas kelas (class_id) yang konsisten, kemudian membaca setiap pasangan file gambar (.jpg) dan file label (.txt). File label berformat YOLO berisi satu atau lebih baris anotasi yang merepresentasikan objek rambu pada gambar. Setiap baris anotasi dibaca untuk memperoleh informasi class_id serta koordinat bounding box dalam format titik tengah dan ukuran kotak. Karena beberapa gambar dapat memuat lebih dari satu rambu, pipeline dirancang untuk memproses multi-objek dalam satu gambar.
Setelah anotasi dibaca, dilakukan tahap konversi anotasi dan pembentukan target pelatihan agar sesuai dengan kebutuhan input YOLOS. Tahap ini mencakup parsing nilai koordinat YOLO dan membentuk struktur data target bounding box yang dipakai pada proses training. Dengan demikian, setiap sampel data pada dataset akan menghasilkan dua komponen utama, yaitu input citra dan target label (kelas dan lokasi objek). Pada saat yang sama, citra dipersiapkan melalui proses prapemrosesan, seperti penyesuaian ukuran dan normalisasi, agar sesuai dengan konfigurasi input model. prapemrosesan ini penting untuk menjaga konsistensi bentuk data yang masuk ke model YOLOS pada saat training maupun prediksi. Alur pipeline persiapan data dan pembentukan target pelatihan untuk YOLOS/ViT ditunjukkan pada Gambar 3.3.
 
Gambar 3.3 Alur Pipeline Persiapan Data untuk Pelatihan Model YOLOS/ViT
Pada tahapan pelatihan model, YOLOS digunakan sebagai model deteksi objek yang menghasilkan keluaran berupa prediksi bounding box dan klasifikasi kelas untuk setiap objek yang terdeteksi. Proses pelatihan dilakukan pada subset train, dengan konfigurasi pelatihan disesuaikan terhadap kebutuhan eksperimen, seperti ukuran input gambar, jumlah epoch, serta parameter optimisasi. Selama training berlangsung, model mempelajari representasi visual rambu lalu lintas dari data latih dan menyesuaikan bobot parameter agar mampu menghasilkan prediksi yang sesuai dengan anotasi. Setelah training selesai, model disimpan ke direktori backend/models menggunakan penamaan berbasis versi untuk memudahkan pengelolaan hasil eksperimen.
Agar sistem mendukung pergantian model, dirancang mekanisme manajemen model yang mencatat informasi model dalam SQLite. Informasi yang disimpan mencakup versi model, lokasi penyimpanan, dan status model aktif. Dengan mekanisme ini, sistem dapat memilih model yang akan digunakan pada proses prediksi tanpa perlu melakukan perubahan manual pada kode. Pemilihan model aktif menjadi penting ketika terdapat beberapa model hasil pelatihan dan diperlukan penggunaan model tertentu yang dianggap paling sesuai untuk kebutuhan prediksi.
Tahap terakhir pada pipeline adalah prediksi menggunakan model aktif. Pada proses ini, pengguna mengunggah gambar statis melalui antarmuka web, kemudian backend memuat model yang ditetapkan sebagai model aktif dari direktori penyimpanan. Gambar di-preprocess dengan langkah yang konsisten dengan training, lalu dilakukan inferensi menggunakan YOLOS untuk menghasilkan keluaran berupa bounding box, label kelas, dan confidence score. Hasil tersebut kemudian dikembalikan ke frontend untuk divisualisasikan, sehingga pengguna dapat melihat posisi rambu yang terdeteksi beserta jenis rambu yang dikenali oleh sistem. Dengan pipeline ini, metode yang dirancang mampu mendukung kebutuhan penelitian dalam membangun prototipe deteksi dan klasifikasi rambu lalu lintas berbasis Vision Transformer berbasis unggah gambar.



3.5 Perancangan Arsitektur Sistem 
Arsitektur sistem pada penelitian ini dirancang sebagai prototipe berbasis web yang memisahkan tanggung jawab antara antarmuka pengguna, layanan pemrosesan, dan penyimpanan metadata model. Pemisahan ini bertujuan agar proses training dan prediksi model YOLOS/ViT dapat dijalankan secara terstruktur, mudah dikembangkan, serta konsisten ketika dijalankan pada lingkungan lokal. Secara umum, arsitektur terdiri dari empat komponen utama, yaitu Frontend (React), Backend (FastAPI + Model YOLOS/ViT), Database (SQLite), dan Docker sebagai lingkungan eksekusi. Arsitektur Sistem Deteksi dan Klasifikasi Rambu Lalu Lintas yang diusulkan ditunjukkan pada Gambar 3.4.
 
Gambar 3.4 Arsitektur Sistem Deteksi dan Klasifikasi Rambu Lalu Lintas

Komponen frontend dibangun menggunakan React dan berperan sebagai antarmuka pengguna untuk menjalankan fitur utama sistem. Antarmuka menyediakan halaman untuk melakukan training, memilih model aktif, serta melakukan prediksi melalui unggah gambar. Frontend berkomunikasi dengan backend melalui request HTTP untuk mengirim data dan menerima respons hasil pemrosesan dari backend. Dengan desain berbasis web, pengguna cukup berinteraksi melalui browser tanpa perlu menjalankan proses model secara manual.
Komponen backend dikembangkan menggunakan FastAPI sebagai layanan yang menangani proses inti penelitian, yaitu pelatihan dan inferensi model YOLOS/ViT. Pada fitur training, backend memuat dataset dari struktur folder yang tersedia, memproses anotasi YOLO, menjalankan pipeline pelatihan, dan menyimpan model hasil training. Pada fitur prediksi, backend menerima gambar yang diunggah pengguna, melakukan prapemrosesan, memuat model yang sedang aktif, menjalankan inferensi, lalu mengembalikan hasil deteksi berupa bounding box, label kelas, dan confidence score. Backend juga menyediakan layanan manajemen model yang menampilkan daftar model versi dan mendukung penetapan model aktif yang akan digunakan untuk prediksi.
Untuk mendukung pergantian model dan pencatatan hasil eksperimen, sistem menggunakan SQLite sebagai penyimpanan metadata model. Database ini menyimpan informasi seperti nama/versi model, lokasi folder penyimpanan model pada direktori backend/models, serta penanda model mana yang sedang aktif. Dengan penyimpanan metadata tersebut, proses pemilihan model tidak bergantung pada perubahan kode, dan sistem dapat mempertahankan riwayat versi model hasil training. Pemilihan model aktif dari SQLite menjadi acuan backend saat melakukan prediksi, sehingga hasil inferensi selalu menggunakan model yang ditetapkan.
Seluruh komponen dijalankan pada lingkungan lokal menggunakan Docker untuk memastikan konsistensi konfigurasi dan dependensi. Docker membantu mengelola dependensi Python serta dependensi frontend React dalam lingkungan yang terisolasi. Dengan arsitektur ini, sistem dapat dijalankan dan direplikasi dengan lebih mudah pada perangkat lain, sekaligus mengurangi risiko perbedaan environment yang dapat memengaruhi proses training maupun prediksi. Selain itu, penggunaan Docker memudahkan pengembangan bertahap karena setiap komponen dapat dikelola sebagai layanan yang terpisah namun tetap terintegrasi melalui jaringan container.

3.6 Perancangan UML
3.6.1 Use Case Diagram
Use case pada sistem berfokus pada dua proses utama: training model dan prediksi. Admin memiliki use case untuk melihat daftar kelas yang tersedia, menjalankan training, melihat daftar model hasil training, serta memilih model aktif. Pengguna memiliki use case untuk mengunggah gambar dan memperoleh hasil prediksi. Hasil prediksi yang ditampilkan berupa bounding box, label kelas, dan confidence score. Use case diagram pada sistem ditunjukkan pada Gambar 3.5.
 
Gambar 3.5 Use Case Diagram Prediksi Rambu Lalu Lintas

3.6.2  Activity Diagram Proses Training
Activity diagram proses training menggambarkan langkah-langkah sistem ketika Admin menjalankan pelatihan model. Alur dimulai dari Admin membuka halaman training, kemudian sistem menampilkan daftar kelas yang tersedia. Admin memilih dataset atau kelas yang akan digunakan, lalu menekan tombol training. Backend memuat data dan anotasi, menjalankan proses pelatihan YOLOS/ViT, kemudian menyimpan model hasil training ke direktori backend/models sebagai versi baru. Setelah penyimpanan selesai, sistem mencatat metadata model (versi dan path) ke SQLite, lalu menampilkan status training kepada Admin. Alur proses training ditunjukkan pada Gambar 3.6.
 
Gambar 3.6 Activity Diagram Proses Training

3.6.3 Activity Diagram Proses Prediksi 
Activity diagram proses prediksi menjelaskan alur ketika pengguna melakukan deteksi rambu lalu lintas pada gambar statis. Alur dimulai dari pengguna membuka halaman prediksi dan mengunggah gambar. Backend menerima gambar, memuat model yang sedang aktif berdasarkan informasi pada SQLite, melakukan prapemrosesan, lalu menjalankan inferensi dengan YOLOS untuk menghasilkan keluaran bounding box, label kelas, dan confidence score. Hasil prediksi kemudian dikirim kembali ke frontend dan divisualisasikan pada gambar yang diunggah. Alur proses prediksi ditunjukkan pada Gambar 3.7.
 
Gambar 3.7 Activity Diagram Proses Prediksi
3.6.4 Sequence Diagram Prediksi 
Sequence diagram prediksi menggambarkan interaksi antar komponen sistem saat proses prediksi berlangsung. Urutan komunikasi dimulai dari pengguna melakukan unggah gambar pada frontend, kemudian frontend mengirim request ke backend. Backend memeriksa model aktif pada SQLite, memuat model dari direktori backend/models, melakukan prapemrosesan, menjalankan inferensi, lalu mengembalikan respons hasil prediksi ke frontend. Frontend menampilkan hasil deteksi dalam bentuk visualisasi bounding box beserta label dan confidence score. Diagram ini menegaskan pembagian peran antar komponen, di mana frontend menangani interaksi dan tampilan, sedangkan backend menangani proses model dan pengambilan model aktif. Interaksi antar komponen pada proses prediksi ditunjukkan pada Gambar 3.8.
 
Gambar 3.8 Sequence Diagram Prediksi

3.7 Perancangan Antarmuka
Perancangan antarmuka pada penelitian ini bertujuan untuk menggambarkan tampilan dan alur interaksi pengguna dalam menjalankan fitur utama sistem. Antarmuka dibangun berbasis web agar mudah digunakan melalui browser, serta memfokuskan fungsi pada kebutuhan prototipe, yaitu pengelolaan dataset, proses training model, manajemen model, dan prediksi gambar statis. Struktur menu pada sistem terdiri dari empat bagian utama, yaitu Dashboard, Training & Model, Dataset, dan Prediksi. Rancangan antarmuka untuk setiap menu utama ditunjukkan pada Gambar 3.9 sampai dengan Gambar 3.12.
3.7.1 Dashboard
Menu Dashboard berfungsi sebagai halaman ringkasan untuk menampilkan informasi umum mengenai kondisi sistem. Informasi yang ditampilkan dapat mencakup status model yang sedang aktif, jumlah model yang tersimpan, ringkasan dataset yang tersedia, serta ringkasan aktivitas terakhir seperti training terakhir atau model versi terbaru yang dibuat. Dashboard dirancang untuk membantu pengguna memahami kondisi sistem secara cepat sebelum menjalankan proses training atau prediksi. Rancangan tampilan menu Dashboard ditunjukkan pada Gambar 3.9.

 
Gambar 3.9 Antarmuka Dashboard
3.7.2 Training & Model
Menu Training & Model menyediakan fitur untuk menjalankan proses pelatihan model sekaligus mengelola model yang telah dihasilkan. Pada halaman ini, sistem menampilkan daftar opsi training, tombol untuk memulai training, serta indikator status proses. Setelah training selesai, halaman ini juga menampilkan daftar versi model yang tersimpan pada direktori backend/models, termasuk informasi dasar seperti nama/versi model dan waktu pembuatan. Selain itu, tersedia kontrol untuk menetapkan model aktif yang akan digunakan pada proses prediksi, sehingga pengguna dapat melakukan pergantian model sesuai kebutuhan eksperimen. Rancangan tampilan menu Training & Model ditunjukkan pada Gambar 3.10.
 
Gambar 3.10 Antarmuka Training
3.7.3 Dataset 
Menu Dataset digunakan untuk menampilkan dan memeriksa struktur dataset yang digunakan pada penelitian. Halaman ini menampilkan daftar kelas rambu yang tersedia serta informasi ringkas mengenai isi dataset, misalnya jumlah gambar per kelas atau struktur folder train dan test. Tujuan menu ini adalah memudahkan pengguna memastikan dataset telah tersusun dengan benar, sehingga proses training dapat dijalankan tanpa kendala akibat kesalahan struktur data. Menu Dataset juga dapat berfungsi sebagai sarana validasi awal sebelum training dilakukan. Rancangan tampilan menu Dataset ditunjukkan pada Gambar 3.11.
 
Gambar 3.11 Antarmuka Dataset
3.7.4 Prediksi 
Menu Prediksi merupakan halaman utama untuk melakukan deteksi dan klasifikasi rambu lalu lintas pada gambar statis. Pada halaman ini, pengguna mengunggah gambar melalui komponen upload, kemudian sistem mengirim gambar ke backend untuk diproses menggunakan model yang sedang aktif. Hasil prediksi ditampilkan dalam bentuk visualisasi, yaitu gambar yang diberi bounding box, label kelas rambu, dan confidence score. Halaman ini dirancang sederhana agar pengguna dapat melakukan prediksi berulang kali dengan gambar yang berbeda, serta memastikan hasil deteksi dapat diamati secara langsung setelah proses unggah selesai. Rancangan tampilan menu Prediksi ditunjukkan pada Gambar 3.12.
