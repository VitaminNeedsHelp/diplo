import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "data.json")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

os.makedirs(IMAGES_DIR, exist_ok=True)

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 1280

DEFAULT_SETTINGS = {
    "fullscreen": False,
    "font_size": 16,   # Basis-Schriftgröße
}

# ⚠️ Admin-Passwort – bitte anpassen!
ADMIN_PASSWORD = "admin"