# 🔧 Bengkel Track – Aplikasi Peminjaman Alat Bengkel

## 📌 Deskripsi Proyek

**Bengkel Track** merupakan aplikasi desktop berbasis Python yang dirancang untuk membantu proses pengelolaan administrasi peminjaman dan pengembalian peralatan bengkel.

Aplikasi ini dibuat sebagai solusi digital untuk menggantikan proses pencatatan manual yang berpotensi menyebabkan kesalahan pencatatan, kehilangan data, maupun kesulitan dalam memantau status peminjaman alat.

Dengan aplikasi ini, pengguna dapat mencatat data peminjam, mengelola transaksi pengembalian, memantau kondisi peralatan, serta menyimpan riwayat transaksi secara terstruktur melalui database lokal.

## 🎯 Tujuan Pembuatan

Tujuan utama pengembangan aplikasi Bengkel Track adalah:

- Mempermudah proses pencatatan peminjaman dan pengembalian alat bengkel.
- Mengurangi ketergantungan terhadap pencatatan manual menggunakan kertas.
- Membantu memantau status peralatan yang sedang dipinjam maupun sudah dikembalikan.
- Mempermudah dokumentasi kondisi alat ketika proses pengembalian.
- Menyediakan penyimpanan data yang terstruktur dan mudah diakses.
- Menerapkan ilmu pemrograman Python dan pengelolaan database ke dalam proyek nyata.

## ⚙️ Fitur Utama

### 1. Dashboard
Menampilkan ringkasan aktivitas transaksi, meliputi:
- Jumlah transaksi peminjaman aktif.
- Jumlah transaksi yang sudah dikembalikan.
- Jumlah transaksi dengan laporan kerusakan.
- Total keseluruhan transaksi.
- Daftar peminjaman terbaru.

### 2. Manajemen Peminjaman
Digunakan untuk mencatat transaksi peminjaman peralatan bengkel dengan informasi:
- Nama peminjam.
- Kelas peminjam.
- Nama peralatan.
- Jumlah peralatan.
- Tanggal dan waktu peminjaman otomatis.

### 3. Manajemen Pengembalian
Digunakan untuk mencatat proses pengembalian peralatan dengan informasi:
- Data transaksi peminjaman yang akan dikembalikan.
- Nama penanggung jawab alat.
- Jumlah alat yang dikembalikan.
- Status kondisi alat (rusak atau tidak).
- Keterangan kerusakan.
- Tanggal dan waktu pengembalian otomatis.

Setelah transaksi pengembalian berhasil disimpan, status peminjaman akan diperbarui secara otomatis.

### 4. Riwayat Transaksi
Menyediakan dokumentasi seluruh transaksi peminjaman dan pengembalian yang telah dilakukan.

Tersedia fitur ekspor data ke format CSV untuk mempermudah pembuatan laporan dan pengolahan data menggunakan aplikasi spreadsheet.

## 🛠️ Teknologi yang Digunakan

| Teknologi | Kegunaan |
|---|---|
| Python | Bahasa pemrograman utama |
| Tkinter | Membangun antarmuka aplikasi desktop |
| SQLite | Database penyimpanan data lokal |
| CSV | Ekspor laporan transaksi |
| Datetime | Mengelola tanggal dan waktu transaksi |

## 💾 Sistem Penyimpanan Data

Aplikasi menggunakan SQLite sebagai sistem database lokal. Seluruh informasi peminjaman dan pengembalian disimpan dalam file `bengkel_track.db`.

Database terdiri dari dua tabel utama:
- `peminjaman` – Menyimpan informasi identitas peminjam, alat, jumlah, waktu, dan status peminjaman.
- `pengembalian` – Menyimpan informasi pengembalian, penanggung jawab, jumlah alat, kondisi kerusakan, dan waktu pengembalian.

Penyimpanan lokal memungkinkan aplikasi digunakan tanpa memerlukan koneksi internet maupun server database terpisah.

## 🎨 Tampilan Antarmuka

Aplikasi menggunakan kombinasi warna merah, hitam, dan putih dengan konsep tampilan modern dan sederhana. Antarmuka dibangun menggunakan Tkinter agar pengguna dapat mengoperasikan aplikasi melalui tampilan grafis tanpa harus berinteraksi langsung dengan terminal.

## 🚀 Manfaat Aplikasi

Dengan adanya Bengkel Track, proses administrasi peralatan bengkel diharapkan menjadi lebih terstruktur, efisien, dan mudah dipantau. Aplikasi ini juga membantu penanggung jawab dalam melakukan dokumentasi transaksi serta mengetahui kondisi peralatan setelah digunakan.

## 🔮 Pengembangan Selanjutnya

Beberapa pengembangan yang berpotensi ditambahkan:
- Sistem autentikasi dan login pengguna.
- Manajemen inventaris dan stok peralatan.
- Fitur pencarian dan filter transaksi.
- Pencetakan bukti peminjaman dan pengembalian.
- Backup dan pemulihan database.
- Pengembangan sistem ke jaringan lokal atau cloud.

---

**Bengkel Track**  
*Digitalisasi Administrasi Peminjaman dan Pengembalian Alat Bengkel.*

Developed with Python 🐍
