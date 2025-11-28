# 📘 Raspberry Pi Tutorial System

Ein Touch-optimiertes Python GUI zur Anzeige & Verwaltung von Schritt-für-Schritt-Tutorials

---

## 🖥️ Überblick

Dieses Projekt ist ein vollständiges **Tutorial-Anzeige- und Verwaltungssystem** für den Raspberry Pi im **Hochformat** (z. B. 720×1280).  
Es ist optimiert für:

- Touchscreens
- Produktions-/Werkstattumgebungen
- Schulungs- und Infoterminals
- Kiosk-Modus / Vollbildbetrieb

Die App bietet einen **Admin-Modus**, einen **Editor**, einen **Viewer** und speichert alles automatisch in einer JSON-Datei.

---

# 🚀 Features

## 👁️ Tutorial-Viewer

- Darstellung eines Tutorials mit:
  - Titel
  - Bild (PNG/JPG/GIF)
  - Beschreibungstext
- Navigation **Vor / Zurück**
- Layout optimiert für Hochformat

---

## 📝 Tutorial-Editor (nur Admin)

- Bearbeiten des Tutorial-Namens
- Pro Seite:
  - Seitentitel
  - Bild auswählen
  - Beschreibungstext
- **Seite hinzufügen**
- Seiten-Navigation
- Änderungen speichern

---

## 🔐 Admin-Modus

### Unsichtbarer Login

- Auf dem Home-Screen **5× innerhalb von 5 Sekunden** auf „Tutorial-Home“ klicken
- Passwort eingeben → Admin-Modus wird aktiviert

### Admin-Funktionen:

- Neues Tutorial erstellen
- Tutorials bearbeiten
- Tutorials löschen

### Logout:

- Über das **Einstellungsmenü**

---

# 🏠 Home-Screen

- Liste aller Tutorials
- **Doppelklick** auf ein Tutorial → öffnet den Viewer
- Buttons:
  - Tutorial anzeigen
  - (Admin) Neues Tutorial
  - (Admin) Bearbeiten
  - (Admin) Löschen
  - Einstellungen

---

# ⚙️ Einstellungen

- Vollbildmodus an/aus
- Schriftgröße einstellen
- Admin-Logout
- Einstellungen werden in `data.json` gespeichert

---

# 💾 Datenverwaltung

- Alle Tutorials und Einstellungen werden in `data.json` gespeichert
- Bilder werden im `images/`-Ordner gespeichert
- Automatisches Laden und Speichern
- Einfache JSON-Struktur für Tutorials
- Einfache Erweiterbarkeit
- Backup- und Wiederherstellungsfunktionen

---

# 🛠️ Installation & Nutzung

1. **Voraussetzungen**:
   - Raspberry Pi mit installiertem Raspbian OS
   - Python 3.x
   - Tkinter-Bibliothek (normalerweise vorinstalliert)
   - Pillow-Bibliothek (`pip install Pillow`)
2. **Projekt herunterladen**:
   - Git-Repository klonen oder ZIP herunterladen und entpacken

- `git clone <repository-url>`

3. **Projektverzeichnis wechseln**:
   - `cd <projekt-verzeichnis>`
4. **App starten**:
   - `python3 main.py`
5. **App verwenden**:
   - Tutorials im Home-Screen anzeigen
   - Admin-Modus über unsichtbaren Login betreten
   - Tutorials erstellen, bearbeiten und löschen

---
