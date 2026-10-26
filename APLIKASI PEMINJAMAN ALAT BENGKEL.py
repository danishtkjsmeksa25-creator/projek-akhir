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
