import csv
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from pathlib import Path

APP_TITLE = "List Peminjaman Alat Bengkel"
DB_FILE = Path(__file__).with_name("bengkel_track.db")

# Warna Layout!
BG = "#101114"
PANEL = "#1B1C21"
PANEL_2 = "#25262D"
RED = "#E32636"
RED_DARK = "#B51220"
WHITE = "#F5F5F5"
MUTED = "#B5B7C0"
GREEN = "#37C978"
YELLOW = "#F4C542"


class BengkelTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_TITLE} | Manajemen Alat Bengkel")
        self.root.geometry("1120x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)

        self.db = sqlite3.connect(DB_FILE)
        self.db.row_factory = sqlite3.Row
        self.create_tables()
        self.setup_style()
        self.build_layout()
        self.refresh_all()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    # Database awal! 
    def create_tables(self):
        """Membuat tabel database jika belum tersedia."""
        with self.db:
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS peminjaman (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    kelas TEXT NOT NULL,
                    waktu_pinjam TEXT NOT NULL,
                    daftar_alat TEXT NOT NULL,
                    total_alat INTEGER NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Dipinjam'
                )
            """)
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS pengembalian (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    peminjaman_id INTEGER NOT NULL UNIQUE,
                    penanggung_jawab TEXT NOT NULL,
                    total_alat INTEGER NOT NULL,
                    ada_kerusakan TEXT NOT NULL,
                    keterangan TEXT,
                    waktu_kembali TEXT NOT NULL,
                    FOREIGN KEY (peminjaman_id) REFERENCES peminjaman(id)
                )
            """)
