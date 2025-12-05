import json
import os
from config import SETTINGS_FILE, DEFAULT_SETTINGS

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            s = json.load(f)
    except Exception:
        s = DEFAULT_SETTINGS.copy()

    # Fehlende Defaults ergänzen
    for k, v in DEFAULT_SETTINGS.items():
        s.setdefault(k, v)

    return s


def save_settings(settings: dict):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Fehler beim Speichern der Einstellungen:", e)
