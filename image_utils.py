import os
import tkinter as tk

# Pillow optional verwenden
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


def load_image_for_tk(path, max_width=None, max_height=None):
    """
    Lädt ein Bild und gibt ein Tk-PhotoImage-Objekt zurück oder None.
    - Erwartet: 'path' ist ein gültiger Dateipfad (absolut oder relativ, wie vom Aufrufer gegeben).
    - Wenn Pillow verfügbar, wird optional skaliert.
    - Falls kein Pillow, wird tk.PhotoImage verwendet (unterstützt PNG/GIF; JPEG nur mit Pillow).
    """
    if not path:
        return None

    # Falls relativer Pfad => akzeptieren (Aufrufer sollte richtigen Pfad übergeben)
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

    # Fallback auf tk.PhotoImage (meistens PNG/GIF)
    try:
        img = tk.PhotoImage(file=path)
        return img
    except Exception:
        return None
