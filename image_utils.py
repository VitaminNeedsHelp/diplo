import os
import tkinter as tk
from config import IMAGES_DIR

# Pillow optional verwenden
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def load_image_for_tk(path, max_width=None, max_height=None):
    """
    Versucht, ein Bild zu laden und optional zu skalieren.
    - Wenn Pillow verfügbar: skalieren möglich.
    - Sonst: tk.PhotoImage (PNG/GIF), ohne Skalierung.
    Gibt ein Tk-Image-Objekt zurück oder None.
    """
    if not path:
        return None
    if not os.path.isabs(path):
        path = os.path.join(IMAGES_DIR, path)
    if not os.path.exists(path):
        return None

    if PIL_AVAILABLE:
        try:
            img = Image.open(path)
            if max_width and max_height:
                img.thumbnail((max_width, max_height), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    try:
        img = tk.PhotoImage(file=path)  # PNG/GIF
        return img
    except Exception:
        return None
