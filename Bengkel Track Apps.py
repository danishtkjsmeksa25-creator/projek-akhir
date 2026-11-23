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

    # Dashboard!
    def build_dashboard(self):
        page = self.pages["Dashboard"]
        self.page_title(page, "Dashboard", "Ringkasan aktivitas peminjaman alat bengkel.")

        cards = tk.Frame(page, bg=BG)
        cards.pack(fill="x")
        self.stat_labels = {}
        stats = [
            ("Dipinjam", "0", RED),
            ("Sudah kembali", "0", GREEN),
            ("Alat rusak", "0", YELLOW),
            ("Total transaksi", "0", WHITE),
        ]
        for label, value, color in stats:
            card = tk.Frame(cards, bg=PANEL, padx=18, pady=16)
            card.pack(side="left", fill="both", expand=True, padx=(0, 10))
            tk.Label(card, text=label.upper(), bg=PANEL, fg=MUTED,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w")
            number = tk.Label(card, text=value, bg=PANEL, fg=color,
                              font=("Segoe UI", 25, "bold"))
            number.pack(anchor="w", pady=(7, 0))
            self.stat_labels[label] = number

        tk.Label(
            page, text="PEMINJAMAN TERBARU", bg=BG, fg=WHITE,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(25, 6))
        self.dashboard_tree = self.make_tree(
            page, ("id", "nama", "kelas", "waktu", "alat", "status"),
            ("ID", "Nama Peminjam", "Kelas", "Jam Peminjaman", "Daftar Alat", "Status"),
            (50, 170, 100, 170, 300, 110)
        )

    # Formulir Peminjaman!
    def build_peminjaman(self):
        page = self.pages["Peminjaman"]
        self.page_title(page, "Peminjaman Alat", "Isi data peminjam dan alat yang dibawa.")

        form = tk.Frame(page, bg=PANEL, padx=20, pady=16)
        form.pack(fill="x")
        self.nama_var = tk.StringVar()
        self.kelas_var = tk.StringVar()
        self.alat_var = tk.StringVar()
        self.jumlah_var = tk.StringVar(value="1")

        self.make_label(form, "Nama peminjam")
        self.make_entry(form, self.nama_var, 45).pack(anchor="w", ipady=7)
        self.make_label(form, "Kelas")
        self.make_entry(form, self.kelas_var, 25).pack(anchor="w", ipady=7)

        row = tk.Frame(form, bg=PANEL)
        row.pack(fill="x", pady=(0, 5))
        left = tk.Frame(row, bg=PANEL)
        left.pack(side="left", fill="x", expand=True, padx=(0, 12))
        right = tk.Frame(row, bg=PANEL)
        right.pack(side="left")
        self.make_label(left, "Nama alat")
        self.make_entry(left, self.alat_var, 40).pack(anchor="w", ipady=7)
        self.make_label(right, "Jumlah")
        self.make_entry(right, self.jumlah_var, 10).pack(anchor="w", ipady=7)

        self.make_button(form, "＋  Simpan Peminjaman", self.save_peminjaman).pack(
            anchor="w", pady=(14, 0)
        )

        tk.Label(page, text="DAFTAR PEMINJAMAN AKTIF", bg=BG, fg=WHITE,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(18, 0))
        self.loan_tree = self.make_tree(
            page, ("id", "nama", "kelas", "waktu", "alat", "total"),
            ("ID", "Nama", "Kelas", "Jam Pinjam", "Daftar Alat", "Total Alat"),
            (50, 160, 100, 165, 350, 90)
        )

    def save_peminjaman(self):
        nama = self.nama_var.get().strip()
        kelas = self.kelas_var.get().strip()
        alat = self.alat_var.get().strip()
        jumlah_text = self.jumlah_var.get().strip()

        if not nama or not kelas or not alat or not jumlah_text:
            messagebox.showwarning("Data belum lengkap", "Isi nama, kelas, nama alat, dan jumlah.")
            return
        try:
            jumlah = int(jumlah_text)
            if jumlah < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Jumlah tidak valid", "Jumlah alat harus berupa angka minimal 1.")
            return

        waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with self.db:
            self.db.execute("""
                INSERT INTO peminjaman (nama, kelas, waktu_pinjam, daftar_alat, total_alat, status)
                VALUES (?, ?, ?, ?, ?, 'Dipinjam')
            """, (nama, kelas, waktu, f"{alat} (jumlah {jumlah})", jumlah))

        self.nama_var.set("")
        self.kelas_var.set("")
        self.alat_var.set("")
        self.jumlah_var.set("1")
        messagebox.showinfo("Berhasil", "Data peminjaman berhasil disimpan.")
        self.refresh_all()

    # Formulir Pengembalian!
    def build_pengembalian(self):
        page = self.pages["Pengembalian"]
        self.page_title(page, "Pengembalian Alat", "Pilih transaksi aktif, lalu catat kondisi alat.")

        form = tk.Frame(page, bg=PANEL, padx=20, pady=16)
        form.pack(fill="x")
        self.loan_choice = tk.StringVar()
        self.return_person_var = tk.StringVar()
        self.return_total_var = tk.StringVar()
        self.damage_var = tk.StringVar(value="Tidak")
        self.damage_note_var = tk.StringVar()

        self.make_label(form, "Pilih peminjaman yang akan dikembalikan")
        self.loan_combo = ttk.Combobox(
            form, textvariable=self.loan_choice, state="readonly", width=75
        )
        self.loan_combo.pack(anchor="w", ipady=5, fill="x")

        self.make_label(form, "Nama penanggung jawab alat")
        self.make_entry(form, self.return_person_var, 45).pack(anchor="w", ipady=7)

        self.make_label(form, "Total alat yang dikembalikan")
        self.make_entry(form, self.return_total_var, 15).pack(anchor="w", ipady=7)

        self.make_label(form, "Apakah ada kerusakan?")
        ttk.Combobox(
            form, textvariable=self.damage_var, values=("Tidak", "Ya"),
            state="readonly", width=12
        ).pack(anchor="w", ipady=4)

        self.make_label(form, "Keterangan kerusakan (isi jika ada)")
        self.make_entry(form, self.damage_note_var, 60).pack(anchor="w", ipady=7)

        self.make_button(form, "✓  Simpan Pengembalian", self.save_pengembalian).pack(
            anchor="w", pady=(14, 0)
        )

        tk.Label(page, text="RIWAYAT PENGEMBALIAN", bg=BG, fg=WHITE,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(18, 0))
        self.return_tree = self.make_tree(
            page, ("waktu", "person", "total", "damage", "note"),
            ("Waktu Kembali", "Penanggung Jawab", "Total Alat", "Kerusakan", "Keterangan"),
            (170, 200, 100, 110, 350)
        )

    def save_pengembalian(self):
        choice = self.loan_choice.get()
        person = self.return_person_var.get().strip()
        total_text = self.return_total_var.get().strip()
        damage = self.damage_var.get()
        note = self.damage_note_var.get().strip()

        if not choice or not person or not total_text:
            messagebox.showwarning(
                "Data belum lengkap",
                "Pilih peminjaman, isi nama penanggung jawab, dan total alat."
            )
            return
        try:
            total = int(total_text)
            if total < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Jumlah tidak valid", "Total alat harus angka 0 atau lebih.")
            return
        if damage == "Ya" and not note:
            messagebox.showwarning("Keterangan diperlukan", "Tuliskan keterangan kerusakan alat.")
            return

        try:
            loan_id = int(choice.split(" | ")[0].replace("ID ", ""))
        except (ValueError, IndexError):
            messagebox.showerror("Kesalahan", "Pilihan peminjaman tidak terbaca. Pilih ulang.")
            return

        loan = self.db.execute(
            "SELECT * FROM peminjaman WHERE id = ? AND status = 'Dipinjam'", (loan_id,)
        ).fetchone()
        if loan is None:
            messagebox.showwarning("Transaksi tidak tersedia", "Peminjaman ini sudah dikembalikan.")
            self.refresh_all()
            return
        if total > loan["total_alat"]:
            messagebox.showwarning(
                "Jumlah tidak sesuai",
                f"Total yang dikembalikan ({total}) tidak boleh melebihi jumlah pinjaman "
                f"({loan['total_alat']})."
            )
            return

        waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with self.db:
            self.db.execute("""
                INSERT INTO pengembalian
                (peminjaman_id, penanggung_jawab, total_alat, ada_kerusakan, keterangan, waktu_kembali)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (loan_id, person, total, damage, note, waktu))
            self.db.execute(
                "UPDATE peminjaman SET status = 'Dikembalikan' WHERE id = ?", (loan_id,)
            )

        self.return_person_var.set("")
        self.return_total_var.set("")
        self.damage_var.set("Tidak")
        self.damage_note_var.set("")
        messagebox.showinfo("Berhasil", "Data pengembalian berhasil disimpan.")
        self.refresh_all()

    # Riwayat Peminjaman!
    def build_riwayat(self):
        page = self.pages["Riwayat"]
        self.page_title(page, "Riwayat Transaksi", "Semua transaksi tersimpan di database lokal.")
        actions = tk.Frame(page, bg=BG)
        actions.pack(fill="x")
        self.make_button(actions, "Ekspor Peminjaman CSV", self.export_peminjaman).pack(
            side="left", padx=(0, 8)
        )
        self.make_button(actions, "Ekspor Pengembalian CSV", self.export_pengembalian,
                         color=RED_DARK).pack(side="left")
        tk.Label(page, text="DATA PEMINJAMAN", bg=BG, fg=WHITE,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(18, 0))
        self.history_loan_tree = self.make_tree(
            page, ("id", "nama", "kelas", "waktu", "alat", "total", "status"),
            ("ID", "Nama", "Kelas", "Waktu Pinjam", "Daftar Alat", "Total", "Status"),
            (45, 130, 90, 150, 270, 65, 110)
        )

    def export_peminjaman(self):
        rows = self.db.execute("SELECT * FROM peminjaman ORDER BY id DESC").fetchall()
        if not rows:
            messagebox.showinfo("Belum ada data", "Belum ada data peminjaman untuk diekspor.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")],
            initialfile="laporan_peminjaman.csv"
        )
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Nama", "Kelas", "Waktu Pinjam", "Daftar Alat", "Total Alat", "Status"])
            for row in rows:
                writer.writerow([row["id"], row["nama"], row["kelas"], row["waktu_pinjam"],
                                 row["daftar_alat"], row["total_alat"], row["status"]])
        messagebox.showinfo("Ekspor berhasil", f"Laporan disimpan di:\n{path}")

    def export_pengembalian(self):
        rows = self.db.execute("""
            SELECT p.id, r.penanggung_jawab, r.total_alat, r.ada_kerusakan,
                   r.keterangan, r.waktu_kembali
            FROM pengembalian r JOIN peminjaman p ON p.id = r.peminjaman_id
            ORDER BY r.id DESC
        """).fetchall()
        if not rows:
            messagebox.showinfo("Belum ada data", "Belum ada data pengembalian untuk diekspor.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")],
            initialfile="laporan_pengembalian.csv"
        )
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["ID Peminjaman", "Penanggung Jawab", "Total Alat",
                             "Ada Kerusakan", "Keterangan", "Waktu Kembali"])
            for row in rows:
                writer.writerow([row["id"], row["penanggung_jawab"], row["total_alat"],
                                 row["ada_kerusakan"], row["keterangan"], row["waktu_kembali"]])
        messagebox.showinfo("Ekspor berhasil", f"Laporan disimpan di:\n{path}")

    # Fungsi Refresh Status Peminjaman!
    def clear_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def refresh_all(self):
        if not hasattr(self, "dashboard_tree"):
            return

        active = self.db.execute(
            "SELECT COUNT(*) AS n FROM peminjaman WHERE status='Dipinjam'"
        ).fetchone()["n"]
        returned = self.db.execute(
            "SELECT COUNT(*) AS n FROM pengembalian"
        ).fetchone()["n"]
        damaged = self.db.execute(
            "SELECT COUNT(*) AS n FROM pengembalian WHERE ada_kerusakan='Ya'"
        ).fetchone()["n"]
        total = self.db.execute(
            "SELECT COUNT(*) AS n FROM peminjaman"
        ).fetchone()["n"]

        self.stat_labels["Dipinjam"].configure(text=str(active))
        self.stat_labels["Sudah kembali"].configure(text=str(returned))
        self.stat_labels["Alat rusak"].configure(text=str(damaged))
        self.stat_labels["Total transaksi"].configure(text=str(total))

        recent = self.db.execute("SELECT * FROM peminjaman ORDER BY id DESC LIMIT 12").fetchall()
        self.clear_tree(self.dashboard_tree)
        for row in recent:
            self.dashboard_tree.insert("", "end", values=(
                row["id"], row["nama"], row["kelas"], row["waktu_pinjam"],
                row["daftar_alat"], row["status"]
            ))

        active_rows = self.db.execute(
            "SELECT * FROM peminjaman WHERE status='Dipinjam' ORDER BY id DESC"
        ).fetchall()
        self.clear_tree(self.loan_tree)
        combo_values = []
        for row in active_rows:
            self.loan_tree.insert("", "end", values=(
                row["id"], row["nama"], row["kelas"], row["waktu_pinjam"],
                row["daftar_alat"], row["total_alat"]
            ))
            combo_values.append(
                f"ID {row['id']} | {row['nama']} | {row['kelas']} | {row['daftar_alat']}"
            )
        self.loan_combo["values"] = combo_values
        if self.loan_choice.get() not in combo_values:
            self.loan_choice.set(combo_values[0] if combo_values else "")

        returned_rows = self.db.execute("""
            SELECT * FROM pengembalian ORDER BY id DESC
        """).fetchall()
        self.clear_tree(self.return_tree)
        for row in returned_rows:
            self.return_tree.insert("", "end", values=(
                row["waktu_kembali"], row["penanggung_jawab"], row["total_alat"],
                row["ada_kerusakan"], row["keterangan"] or "-"
            ))

        all_rows = self.db.execute("SELECT * FROM peminjaman ORDER BY id DESC").fetchall()
        self.clear_tree(self.history_loan_tree)
        for row in all_rows:
            self.history_loan_tree.insert("", "end", values=(
                row["id"], row["nama"], row["kelas"], row["waktu_pinjam"],
                row["daftar_alat"], row["total_alat"], row["status"]
            ))

    def close_app(self):
        self.db.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = BengkelTrackApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
