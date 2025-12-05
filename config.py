import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Root index file (Einstellungen + Liste der Tutorials)
CONFIG_DIR = os.path.join(BASE_DIR, "config")
os.makedirs(CONFIG_DIR, exist_ok=True)

SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")

DATA_FILE = os.path.join(BASE_DIR, "data.json")

# Root folder für alle Tutorials
TUTORIALS_DIR = os.path.join(BASE_DIR, "tutorials")
os.makedirs(TUTORIALS_DIR, exist_ok=True)

PRIMARY_BG = "#4366E6"   # Ultramarinblau
PRIMARY_FG = "#FFFFFF"

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 1280

DEFAULT_SETTINGS = {
    "fullscreen": False,
    "font_size": 16,   # Basis-Schriftgröße
}

# ⚠️ Admin-Passwort – bitte anpassen!
ADMIN_PASSWORD = "admin"