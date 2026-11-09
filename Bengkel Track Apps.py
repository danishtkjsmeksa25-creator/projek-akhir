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

    #  Layout!
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview", background=PANEL, foreground=WHITE,
            fieldbackground=PANEL, rowheight=30, borderwidth=0
        )
        style.configure(
            "Treeview.Heading", background=RED_DARK,
            foreground=WHITE, font=("Segoe UI", 10, "bold"), padding=8
        )
        style.map("Treeview", background=[("selected", RED_DARK)])
        style.configure("TCombobox", fieldbackground=PANEL_2, foreground=WHITE)

    def build_layout(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=22, pady=(18, 10))

        logo = tk.Label(header,
            text="TKJ",
            bg=RED,
            fg=WHITE,
            font=("Segoe UI", 18, "bold"),
            width=4,
            height=2
        )
        logo.pack(side="left", padx=(0, 12))

        title_box = tk.Frame(header, bg=BG)
        title_box.pack(side="left", fill="y")
        tk.Label(
            title_box, text=APP_TITLE, bg=BG, fg=WHITE,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")
        tk.Label(
            title_box, text="List Peminjaman Alat Bengkel",
            bg=BG, fg=MUTED, font=("Segoe UI", 9)
        ).pack(anchor="w")

        tk.Label(
            header, text="SMK NEGERI 1 KOTA KEDIRI", bg=BG, fg=RED,
            font=("Segoe UI", 10, "bold")
        ).pack(side="right", anchor="center")

        self.nav = tk.Frame(self.root, bg=PANEL)
        self.nav.pack(fill="x", padx=22, pady=(0, 12))

        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True, padx=22, pady=(0, 18))

        self.pages = {}
        for name in ("Dashboard", "Peminjaman", "Pengembalian", "Riwayat"):
            self.pages[name] = tk.Frame(container, bg=BG)
            self.make_button(
                self.nav, name, lambda n=name: self.show_page(n), color=PANEL_2
            ).pack(side="left", padx=(6, 0), pady=6)

        self.build_dashboard()
        self.build_peminjaman()
        self.build_pengembalian()
        self.build_riwayat()
        self.show_page("Dashboard")

    def page_title(self, parent, heading, subtitle):
        tk.Label(
            parent, text=heading, bg=BG, fg=WHITE,
            font=("Segoe UI", 19, "bold")
        ).pack(anchor="w", pady=(0, 3))
        tk.Label(
            parent, text=subtitle, bg=BG, fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(0, 16))

    def show_page(self, name):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[name].pack(fill="both", expand=True)
        self.refresh_all()

    def make_button(self, parent, text, command, color=RED):
        return tk.Button(
            parent, text=text, command=command, bg=color, fg=WHITE,
            activebackground=RED_DARK, activeforeground=WHITE,
            relief="flat", bd=0, padx=15, pady=9,
            font=("Segoe UI", 10, "bold"), cursor="hand2"
        )

    def make_entry(self, parent, variable=None, width=30):
        entry = tk.Entry(
            parent, textvariable=variable, width=width,
            bg=PANEL_2, fg=WHITE, insertbackground=WHITE,
            relief="flat", font=("Segoe UI", 10)
        )
        entry.configure(highlightthickness=1, highlightbackground="#41434B",
                        highlightcolor=RED)
        return entry

    def make_label(self, parent, text):
        tk.Label(
            parent, text=text, bg=BG, fg=MUTED,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 4))

    def make_tree(self, parent, columns, headings, widths):
        holder = tk.Frame(parent, bg=BG)
        holder.pack(fill="both", expand=True, pady=(10, 0))
        tree = ttk.Treeview(holder, columns=columns, show="headings")
        for col, heading, width in zip(columns, headings, widths):
            tree.heading(col, text=heading)
            tree.column(col, width=width, minwidth=70, anchor="w")
        scroll = ttk.Scrollbar(holder, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return tree

