import os
import json
import time
import shutil
from config import BASE_DATA_DIR


# -------- interne Hilfsfunktionen --------

def _slugify(name: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in name).strip("_")


def _ensure_dirs():
    for sub in ("tutorials", "quizzes", "gemischt"):
        os.makedirs(os.path.join(BASE_DATA_DIR, sub), exist_ok=True)


def _base_dir_for_kind(kind: str) -> str:
    if kind == "quiz":
        return os.path.join(BASE_DATA_DIR, "quizzes")
    if kind == "gemischt":
        return os.path.join(BASE_DATA_DIR, "gemischt")
    return os.path.join(BASE_DATA_DIR, "tutorials")


def _tutorial_folder(tid: str):
    _ensure_dirs()
    for base in ("tutorials", "quizzes", "gemischt"):
        base_path = os.path.join(BASE_DATA_DIR, base)
        if not os.path.isdir(base_path):
            continue
        for name in os.listdir(base_path):
            if name.endswith(f"__{tid}"):
                return os.path.join(base_path, name)
    return None


# -------- Öffentliche API (bestehende Signaturen!) --------

def scan_tutorials():
    """
    Scannt alle Tutorial-Ordner und gibt Meta-Liste zurück.
    """
    _ensure_dirs()
    metas = []

    for kind in ("tutorials", "quizzes", "gemischt"):
        base = os.path.join(BASE_DATA_DIR, kind)
        for entry in os.listdir(base):
            folder = os.path.join(base, entry)
            if not os.path.isdir(folder):
                continue

            data_path = os.path.join(folder, "data.json")
            try:
                with open(data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue

            metas.append({
                "id": str(data.get("id")),
                "name": data.get("name", entry),
                "kind": data.get("kind", kind),
                "folder": folder
            })

    return metas


def create_tutorial(name="Neues Tutorial", kind="tutorial", first_page_type="content"):
    """
    Erstellt neues Tutorial und gibt Meta-Dict zurück.
    """
    _ensure_dirs()

    tid = str(int(time.time() * 1000))
    safe_name = _slugify(name)
    base = _base_dir_for_kind(kind)
    folder = os.path.join(base, f"{safe_name}__{tid}")
    images = os.path.join(folder, "images")

    os.makedirs(images, exist_ok=True)

    first_page = (
        {
            "type": "quiz",
            "question": "",
            "image": "",
            "options": ["Antwort A", "Antwort B"],
            "correct_index": 0,
            "explanation": ""
        }
        if first_page_type == "quiz"
        else {
            "type": "content",
            "title": "",
            "image": "",
            "text": ""
        }
    )

    data = {
        "id": tid,
        "name": name,
        "kind": kind,
        "pages": [first_page]
    }

    with open(os.path.join(folder, "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return {
        "id": tid,
        "name": name,
        "kind": kind,
        "folder": folder
    }


def read_tutorial_data(tid: str):
    folder = _tutorial_folder(tid)
    if not folder:
        return None
    path = os.path.join(folder, "data.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def write_tutorial_data(tid: str, data: dict):
    folder = _tutorial_folder(tid)
    if not folder:
        return
    path = os.path.join(folder, "data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def delete_tutorial(tid: str):
    folder = _tutorial_folder(tid)
    if folder and os.path.isdir(folder):
        shutil.rmtree(folder, ignore_errors=True)


def tutorial_images_dir(tid: str):
    folder = _tutorial_folder(tid)
    if not folder:
        return None
    path = os.path.join(folder, "images")
    os.makedirs(path, exist_ok=True)
    return path


def copy_image_into_tutorial(tid: str, src_path: str):
    img_dir = tutorial_images_dir(tid)
    if not img_dir:
        raise RuntimeError("Tutorial nicht gefunden")

    base = os.path.basename(src_path)
    name, ext = os.path.splitext(base)
    dst = os.path.join(img_dir, base)

    counter = 1
    while os.path.exists(dst):
        dst = os.path.join(img_dir, f"{name}_{counter}{ext}")
        counter += 1

    shutil.copy2(src_path, dst)
    return os.path.basename(dst)
