# Praktikum Pemrograman Web Lanjut

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![Django](https://img.shields.io/badge/Django-%23092E20.svg?logo=django&logoColor=white)](#)

<h1 align="center">Hi 👋, I'm Fajar Faruq Abdillah</h1>
<h3 align="center">A student at Universitas Muhammadiyah Kalimantan Timur</h3>

- 🌱 I’m currently learning **django**
- 📫 How to reach me **faruqabdillah11@gmail.com**
- ⚡ Fun fact **i play age of empire 2 de**

Website ini adalah proyek untuk mata kuliah Pemrograman Web Lanjut yang dibangun menggunakan framework Django.

## Ada Apa Saja di Website Ini?

1. **Halaman Utama** - Menampilkan ringkasan dari Sistem yang saya buat.
2. **Sistem Pendukung Keputusan (SPK)** - Fitur utama untuk rekomendasi penjurusan dengan metode TOPSIS.


---

## 🚀 Cara Menjalankan Proyek (Panduan Lengkap untuk Ujian)

Berikut adalah langkah-langkah dari awal untuk menjalankan proyek ini di komputer baru.

### **Prasyarat**

Pastikan **Python** dan **Git** sudah terinstal di komputer Anda.

### **1. Clone Repository**

Buka terminal atau command prompt, lalu clone proyek ini dan langsung masuk ke dalam direktorinya.

```shell
  git clone [https://github.com/FajarFaruqAbdillahUMKT/2311102441137_FAJAR-FARUQ-ABDILLAH_DJANGO.git](https://github.com/FajarFaruqAbdillahUMKT/2311102441137_FAJAR-FARUQ-ABDILLAH_DJANGO.git)
```

```shell
  cd 2311102441137_FAJAR-FARUQ-ABDILLAH_DJANGO
```

### **2. Buat dan Aktifkan Virtual Environment**

Sangat penting untuk membuat lingkungan terisolasi agar dependensi proyek tidak tercampur.

```shell
  # Membuat virtual environment bernama .venv
  python -m venv .venv
````

### **3. Install Semua Dependensi**

Gunakan file `requirements.txt` untuk menginstal semua pustaka Python yang dibutuhkan oleh proyek dengan versi yang
tepat.

```shell
    pip install -r requirements.txt
```

### **4. Jalankan Migrasi Database**

Setelah menginstal dependensi, jalankan migrasi untuk membuat struktur database yang diperlukan oleh Django.

```shell
  python manage.py migrate
```

### **5. Buat Superuser (Akun Admin)**

Anda akan membutuhkan akun admin untuk masuk ke halaman `/admin` guna mengelola data.

```shell
  python manage.py createsuperuser
```

### **6. (Opsional) Load Data Awal (Fixtures)**

Jika Anda memiliki data awal (seperti data kriteria, alternatif, atau data dummy mahasiswa) yang disimpan dalam file
fixture (misal: `data_awal.json`), Anda bisa memuatnya dengan perintah:

```shell
  python manage.py loaddata nama_file_fixture.json
```
atau

```shell
  python manage.py loaddata alternatif kriteria mahasiswa nilai_matakuliah
```

### **7. Jalankan Server Django**

Setelah semua langkah di atas selesai, Anda dapat menjalankan server Django untuk melihat aplikasi.

```shell
  python manage.py runserver
```

Buka browser dan akses `http://127.0.0.1:8000/ atau http://localhost:8000/.


