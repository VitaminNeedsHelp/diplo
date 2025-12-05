import json
import os
import time
import shutil
from config import TUTORIALS_DIR

# ---------- JSON Helper ----------
def _read_json_safe(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def _write_json_safe(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------- Tutorial Path Helpers ----------
def tutorial_folder(tid):
    return os.path.join(TUTORIALS_DIR, str(tid))

def tutorial_data_path(tid):
    return os.path.join(tutorial_folder(tid), "data.json")

def tutorial_images_dir(tid):
    return os.path.join(tutorial_folder(tid), "images")

# ---------- NEU: Tutorial-Scan ----------
def scan_tutorials():
    """
    Scannt /tutorials und erzeugt automatisch eine Meta-Liste.
    Keine Root-data.json nötig!
    """
    metas = []
    if not os.path.exists(TUTORIALS_DIR):
        os.makedirs(TUTORIALS_DIR, exist_ok=True)

    for folder_name in sorted(os.listdir(TUTORIALS_DIR)):
        path = os.path.join(TUTORIALS_DIR, folder_name)
        if not os.path.isdir(path):
            continue

        data_path = os.path.join(path, "data.json")
        data = _read_json_safe(data_path) or {}

        tid = data.get("id") or folder_name
        name = data.get("name", f"Tutorial {tid}")

        metas.append({
            "id": str(tid),
            "name": name,
            "folder": path
        })

    return metas

# ---------- Read / Write Tutorial ----------
def read_tutorial_data(tid):
    return _read_json_safe(tutorial_data_path(tid))

def write_tutorial_data(tid, data):
    _write_json_safe(tutorial_data_path(tid), data)

# ---------- Create Tutorial ----------
def create_tutorial(name="Neues Tutorial"):
    tid = str(int(time.time() * 1000))
    folder = tutorial_folder(tid)

    os.makedirs(folder, exist_ok=True)
    os.makedirs(tutorial_images_dir(tid), exist_ok=True)

    data = {
        "id": tid,
        "name": name,
        "pages": [
            {"title": "Seite 1", "image": "", "text": ""}
        ]
    }

    write_tutorial_data(tid, data)

    return {"id": tid, "name": name, "folder": folder}

# ---------- Delete Tutorial ----------
def delete_tutorial(tid):
    folder = tutorial_folder(tid)
    if os.path.exists(folder):
        shutil.rmtree(folder)

# ---------- Copy images ----------
def copy_image_into_tutorial(tid, src):
    if not os.path.exists(src):
        raise FileNotFoundError(src)

    images = tutorial_images_dir(tid)
    os.makedirs(images, exist_ok=True)

    base = os.path.basename(src)
    name, ext = os.path.splitext(base)

    target = os.path.join(images, base)
    counter = 1
    while os.path.exists(target):
        target = os.path.join(images, f"{name}_{counter}{ext}")
        counter += 1

    shutil.copy2(src, target)
    return os.path.basename(target)
