import socket  # Impor modul socket untuk komunikasi jaringan
import threading  # Impor modul threading untuk menjalankan beberapa proses
import tkinter as tk  # Impor tkinter untuk GUI
from tkinter import scrolledtext, ttk  # Impor komponen GUI tambahan dari tkinter
import subprocess  # Impor subprocess untuk menjalankan perintah sistem
import pyautogui  # Impor pyautogui untuk mengambil screenshot
import os  # Impor modul os untuk interaksi dengan sistem operasi

class ServerApp:
    def __init__(self, root):
        self.root = root  # Inisialisasi root window
        self.root.title("Server RDP Sederhana")  # Set judul window
        self.root.geometry("500x600")  # Set ukuran window
        self.root.configure(bg="#f0f0f0")  # Set warna latar belakang window

        # Membuat area teks dengan scrollbar
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, font=("Helvetica", 10), bg="#ffffff", fg="#000000")
        self.text_area.pack(pady=20, padx=20)  # Menempatkan area teks di window

        # Menampilkan alamat IP pada area teks
        local_ip = socket.gethostbyname(socket.gethostname())
        self.text_area.insert(tk.END, f"Selamat datang di RDP Python Sederhana, Alamat IP: {local_ip}\n")

        # Membuat tombol untuk memulai server
        self.start_button = ttk.Button(root, text="Mulai Server", command=self.start_server)
        self.start_button.pack(pady=10)  # Menempatkan tombol di window

        # Membuat tombol untuk menghentikan server
        self.stop_button = ttk.Button(root, text="Hentikan Server", command=self.stop_server)
        self.stop_button.pack(pady=10)  # Menempatkan tombol di window

        self.server_socket = None  # Inisialisasi socket server
        self.client_sockets = []  # Inisialisasi daftar socket klien

        # Styling untuk tombol
        style = ttk.Style()
        style.configure("Start.TButton", font=("Helvetica", 12, "bold"), background="#4CAF50", foreground="black", padding=10, relief="raised", borderwidth=4)
        style.configure("Stop.TButton", font=("Helvetica", 12, "bold"), background="#f44336", foreground="black", padding=10, relief="raised", borderwidth=4)
        style.map("Start.TButton", foreground=[('pressed', 'yellow'), ('active', 'blue')], background=[('pressed', '!disabled', 'black'), ('active', 'white')])
        style.map("Stop.TButton", foreground=[('pressed', 'yellow'), ('active', 'blue')], background=[('pressed', '!disabled', 'black'), ('active', 'white')])

        self.start_button.configure(style="Start.TButton")
        self.stop_button.configure(style="Stop.TButton")

        # Membuat label footer
        self.footer_label = tk.Label(root, text="dibuat oleh audhighasu.com", font=("Arial", 10), bg="#f0f0f0")
        self.footer_label.pack(side=tk.BOTTOM, pady=10)  # Menempatkan label footer di window

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Membuat socket server
        self.server_socket.bind(('0.0.0.0', 8888))  # Mengikat socket ke alamat IP dan port
        self.server_socket.listen(1)  # Server mulai mendengarkan koneksi
        self.text_area.insert(tk.END, "Server berjalan...\n")  # Menampilkan pesan di area teks
        threading.Thread(target=self.accept_connections, daemon=True).start()  # Membuat thread untuk menerima koneksi

    def stop_server(self):
        if self.server_socket:
            for client_socket in self.client_sockets:
                client_socket.close()  # Menutup semua koneksi klien
            self.server_socket.close()  # Menutup socket server
            self.server_socket = None
            self.client_sockets = []  # Mengosongkan daftar klien
            self.text_area.insert(tk.END, "Server dan semua koneksi klien dihentikan.\n")  # Menampilkan pesan server dihentikan

    def accept_connections(self):
        while True:
            try:
                client_socket, addr = self.server_socket.accept()  # Menerima koneksi dari klien
                self.client_sockets.append(client_socket)  # Menambahkan socket klien ke daftar
                self.text_area.insert(tk.END, f"Koneksi diterima dari {addr}\n")  # Menampilkan alamat klien di area teks
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()  # Membuat thread untuk menangani klien
            except socket.error:
                break  # Keluar dari loop jika server dihentikan

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()  # Menerima pesan dari klien
                if message:
                    if message.strip().lower() == "buka notepad":
                        subprocess.Popen(["notepad.exe"])  # Membuka Notepad
                        self.text_area.insert(tk.END, "Perintah untuk membuka Notepad diterima dan dieksekusi.\n")
                    elif message.strip().lower() == "ambil screenshot":
                        screenshot = pyautogui.screenshot()  # Mengambil screenshot
                        screenshot_file = "server_screenshot.png"
                        screenshot.save(screenshot_file)  # Menyimpan screenshot
                        self.text_area.insert(tk.END, "Screenshot layar server diambil dan disimpan.\n")
                        self.send_file(client_socket, screenshot_file)  # Mengirim file screenshot ke klien
                    elif message.strip().lower() == "buka dxdiag":
                        subprocess.Popen(["dxdiag.exe"])  # Membuka Dxdiag
                        self.text_area.insert(tk.END, "Perintah untuk membuka Dxdiag diterima dan dieksekusi.\n")
                    else:
                        self.text_area.insert(tk.END, f"Klien: {message}\n")  # Menampilkan pesan dari klien
            except socket.error:
                self.text_area.insert(tk.END, "Koneksi terputus\n")  # Menampilkan pesan jika koneksi terputus
                client_socket.close()  # Menutup socket klien
                break

    def send_file(self, client_socket, file_path):
        # Kirim nama file terlebih dahulu
        filename = os.path.basename(file_path)
        client_socket.send(f"FILE:{filename}".encode())  # Mengirim informasi nama file
        client_socket.recv(1024)  # Menunggu konfirmasi dari klien

        # Mengirim isi file dalam bentuk binary
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.send(data)
        
        client_socket.send(b'END_OF_FILE')  # Mengirim sinyal akhir file
        self.text_area.insert(tk.END, "Screenshot telah dikirim ke klien.\n")  # Menampilkan pesan bahwa screenshot telah dikirim

if __name__ == "__main__":
    root = tk.Tk()  # Membuat instance Tkinter
    app = ServerApp(root)  # Membuat instance aplikasi server
    root.mainloop()  # Memulai loop utama Tkinter