import socket  # Impor modul socket untuk komunikasi jaringan
import threading  # Impor modul threading untuk eksekusi konkuren
import tkinter as tk  # Impor modul tkinter untuk GUI
from tkinter import scrolledtext, messagebox, ttk  # Impor komponen GUI tambahan dari tkinter
import os  # Impor modul os untuk interaksi dengan sistem operasi

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Desktop Remote Python Sederhana")  # Atur judul jendela
        self.root.geometry("500x700")  # Atur ukuran jendela
        self.root.configure(bg="#2c3e50")  # Atur warna latar belakang jendela

        # Styling
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=6)
        style.configure("TLabel", font=("Helvetica", 12), background="#2c3e50", foreground="white")
        style.configure("TEntry", font=("Helvetica", 12), padding=5)

        # Area teks dengan scrollbar
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, font=("Consolas", 10), bg="#ecf0f1", fg="#2c3e50")
        self.text_area.pack(pady=20, padx=20)

        # Label dan entri IP server
        self.ip_label = ttk.Label(root, text="IP Server:")
        self.ip_label.pack(pady=5)
        self.ip_entry = ttk.Entry(root, width=60)
        self.ip_entry.pack(pady=5)

        # Tombol koneksi
        self.connect_button = ttk.Button(root, text="Sambung", command=self.connect_to_server)
        self.disconnect_button = ttk.Button(root, text="Putus", command=self.disconnect_from_server)
        self.connect_button.pack(pady=5)
        self.disconnect_button.pack(pady=5)

        # Entri pesan dan tombol kirim
        self.entry = ttk.Entry(root, width=60)
        self.entry.pack(pady=5)
        self.send_button = ttk.Button(root, text="Kirim Pesan", command=self.send_message)
        self.send_button.pack(pady=5)

        # Tombol fungsi
        function_buttons_frame = ttk.Frame(root)
        function_buttons_frame.pack(pady=5)
        self.open_notepad_button = ttk.Button(function_buttons_frame, text="Buka Notepad", command=self.open_notepad)
        self.take_screenshot_button = ttk.Button(function_buttons_frame, text="Ambil Screenshot", command=self.take_screenshot)
        self.open_dxdiag_button = ttk.Button(function_buttons_frame, text="Buka Dxdiag", command=self.open_dxdiag)
        self.open_notepad_button.pack(side=tk.LEFT, padx=5)
        self.take_screenshot_button.pack(side=tk.LEFT, padx=5)
        self.open_dxdiag_button.pack(side=tk.LEFT, padx=5)

        # Label footer
        self.footer_label = ttk.Label(root, text="Dibuat oleh audhighasu.com")
        self.footer_label.pack(side=tk.BOTTOM, pady=10)

        self.client_socket = None  # Inisialisasi socket klien sebagai None

    def connect_to_server(self):
        ip_address = self.ip_entry.get()
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip_address, 8888))
            self.text_area.insert(tk.END, f"Terhubung ke server di {ip_address}\n")
            self.receive_messages()
        except Exception as e:
            messagebox.showerror("Kesalahan Koneksi", f"Tidak dapat terhubung ke server: {e}")

    def disconnect_from_server(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            self.text_area.insert(tk.END, "Terputus dari server.\n")

    def send_message(self):
        if self.client_socket:
            message = self.entry.get()
            self.client_socket.sendall(message.encode())
            self.text_area.insert(tk.END, f"Anda: {message}\n")
            self.entry.delete(0, tk.END)

    def open_notepad(self):
        if self.client_socket:
            self.client_socket.sendall("buka notepad".encode())  # Perintah yang dikoreksi untuk sesuai dengan perintah yang diharapkan server
            self.text_area.insert(tk.END, "Perintah untuk membuka Notepad terkirim.\n")

    def take_screenshot(self):
        if self.client_socket:
            self.client_socket.sendall("ambil screenshot".encode())
            self.text_area.insert(tk.END, "Perintah untuk mengambil screenshot terkirim.\n")

    def open_dxdiag(self):
        if self.client_socket:
            self.client_socket.sendall("buka dxdiag".encode())
            self.text_area.insert(tk.END, "Perintah untuk membuka Dxdiag terkirim.\n")

    def receive_messages(self):
        def receive():
            while True:
                try:
                    message = self.client_socket.recv(1024).decode()
                    if message.startswith("FILE:"):
                        filename = message.split(":")[1]
                        self.client_socket.send(b'OK')
                        self.download_file(filename)
                    else:
                        self.text_area.insert(tk.END, f"Server: {message}\n")
                except:
                    self.text_area.insert(tk.END, "Koneksi hilang\n")
                    self.client_socket.close()
                    break

        threading.Thread(target=receive, daemon=True).start()

    def download_file(self, filename):
        with open(filename, 'wb') as file:
            while True:
                data = self.client_socket.recv(1024)
                if data == b'END_OF_FILE':
                    break
                file.write(data)

        self.text_area.insert(tk.END, f"Screenshot disimpan sebagai {filename}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
