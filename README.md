# RDP Controller 🚀

**RDP Controller** adalah aplikasi berbasis Python yang memungkinkan pengguna mengontrol sesi **Remote Desktop Protocol (RDP)** secara otomatis, dengan memanfaatkan 2 aplikasi yang tertanam dimasing-masing komputer agar saling berkomunikasi.

## 📌 Fitur
✅ Mengontrol sesi RDP secara otomatis 🖥️  
✅ Simulasi input mouse & keyboard dengan **PyAutoGUI** 🖱️⌨️  
✅ Mengambil screenshot tampilan RDP menggunakan **Pillow** 📸  
✅ Bisa digunakan dalam **jaringan lokal maupun internet** 🌍  
✅ Mendukung **virtual environment Python dengan Laragon** 🐍

---

## 📂 Instalasi

### 1️⃣ **Clone Repository**
```bash
git clone https://github.com/edisuherlan/Python-RDP-Server-Client
cd RDP-Controller
```

### 2️⃣ **Jalankan Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Untuk Linux & Mac
venv\Scripts\activate     # Untuk Windows
```

### 3️⃣ **Install Dependencies**
```bash
pip install pyautogui
pip install pillow
```

---

## 🚀 Menjalankan Aplikasi
Jalankan script Server terlebih dulu dengan perintah berikut:
```bash
python server.py
```
kemudian jalankan script Client dengan perintah berikut :
```bash
python client.py
```


## 🔧 Membuat Aplikasi Menjadi Executable (.exe)
Untuk mengubah aplikasi server.py ini menjadi executable Windows:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole server.py
```
Hasilnya akan ada di folder `dist/server.exe`.

Untuk mengubah aplikasi server.py ini menjadi executable Windows:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole server.py
```
Hasilnya akan ada di folder `dist/server.exe`.

---

## 📡 Teknologi yang Digunakan
- **Python 3.x** 🐍
- **PyAutoGUI** (Simulasi input keyboard & mouse) 🖱️
- **Pillow** (Mengambil screenshot layar) 📸
- **RDP Protocol (TCP/IP 3389)** 🌍
- **Laragon (Virtual Environment Management)** 🛠️

---

## 🤝 Kontribusi
Jika ingin berkontribusi, silakan fork repository ini, buat branch baru, dan kirimkan pull request! 😊

---

## 📜 Lisensi
Proyek ini menggunakan lisensi **MIT**. Silakan gunakan dan modifikasi sesuai kebutuhan.

---

## 🤝 Penjelasan detail bisa berkunjung ke website berikut :
https://audhighasu.com/2025/03/20/%f0%9f%96%a5%ef%b8%8f%f0%9f%94%a5-remote-desktop-sederhana-dengan-python-dan-laragon/ 😊

---

**🎯 Selamat ngoding! 🚀🔥**
