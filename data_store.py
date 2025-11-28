import json
import time
from config import DATA_FILE, DEFAULT_SETTINGS


def load_data():
    if not DATA_FILE or not isinstance(DATA_FILE, str):
        raise RuntimeError("DATA_FILE ist ungültig.")

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {
            "settings": DEFAULT_SETTINGS.copy(),
            "tutorials": []
        }

    if "settings" not in data:
        data["settings"] = DEFAULT_SETTINGS.copy()
    else:
        for k, v in DEFAULT_SETTINGS.items():
            data["settings"].setdefault(k, v)

    data.setdefault("tutorials", [])
    return data


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Fehler beim Speichern:", e)


def create_empty_tutorial():
    tutorial_id = str(int(time.time()))
    return {
        "id": tutorial_id,
        "name": "Neues Tutorial",
        "pages": [
            {
                "title": "Seite 1",
                "image": "",
                "text": ""
            }
        ]
    }
