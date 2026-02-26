import os

# Basisverzeichnis des Projekts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------- Fenster ----------------
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 900

# ---------------- Farben / Theme ----------------
PRIMARY_BG = "#4366E6"
PRIMARY_FG = "#FFFFFF"

# ---------------- Default Settings ----------------
DEFAULT_SETTINGS = {
    "fullscreen": False,
    "font_size": 16,
}

# ---------------- Admin ----------------
ADMIN_PASSWORD = "admin"

# ---------------- Datenstruktur (NEU) ----------------
# Alle Tutorials / Quizzes liegen ab jetzt hier drunter
BASE_DATA_DIR = os.path.join(BASE_DIR, "tut_data")

# Sicherstellen, dass Basisordner existiert
os.makedirs(BASE_DATA_DIR, exist_ok=True)
