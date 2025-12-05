# 📘 Tutorial Display System – README

Ein touch-optimiertes GUI-System für Raspberry Pi und Windows, mit dem sich Schritt-für-Schritt-Anleitungen („Tutorials“) erstellen, verwalten und anzeigen lassen.  
Alle Tutorials liegen in eigenen Ordnern und sind vollständig unabhängig voneinander.

---

## 🚀 Hauptfunktionen

### ✔ Tutorials anzeigen (Viewer)

- Hochkant-Layout (ideal für Raspberry Pi Touchscreen)
- Jede Seite besteht aus Titel, Bild und Text
- Bilder werden automatisch skaliert
- Navigationsbuttons sind fix am unteren Rand
- Unterstützt beliebig viele Seiten

---

## ✔ Tutorials erstellen & bearbeiten (Editor)

- Nur im Admin-Modus verfügbar
- Funktionen:
  - Tutorialtitel bearbeiten
  - Seiten hinzufügen / wechseln
  - Titel / Bild / Text pro Seite ändern
  - Bilder werden automatisch in den jeweiligen Tutorial-Ordner kopiert
  - Bildvorschau mit automatischer Größenanpassung
  - Save-/Back-Buttons immer sichtbar

---

## ✔ Tutorials verwalten (Home Screen)

- Automatische Ordner-Suche statt globalem Index
- Zeigt alle Tutorials aus dem Ordner `tutorials/`
- Funktionen:
  - Tutorial anzeigen
  - (Admin) Tutorial bearbeiten
  - (Admin) Tutorial löschen
  - (Admin) Neues Tutorial erstellen

---

## 🔐 Admin-Modus

- Aktivierung über 5× Klick auf den Titel
- Passwortabfrage
- Admin-Rechte ermöglichen:
  - Erstellen neuer Tutorials
  - Bearbeiten von Tutorials
  - Löschen von Tutorials
- Deaktivierung über Einstellungen

---

## 🔧 Systemanforderungen

- Raspberry Pi / Linux
  - Python 3
  - Tkinter
  - Pillow (pip install pillow)
- Windows
  - Python 3
  - - Tkinter (bereits enthalten)
  - Pillow

---

## 🎮 Bedienung

- Home Screen
  - Doppelklick auf ein Tutorial → Viewer
  - Admin-Bereich sichtbar, wenn Admin aktiv
- Viewer
  - Navigation über Buttons unten
  - Rückkehr zum Home Screen möglich
- Editor
  - Seiten hinzufügen
  - Bilder auswählen (werden automatisch kopiert)
  - Speichern aktualisiert die data.json des Tutorials
- Einstellungen
  - Vollbildmodus
  - Schriftgröße
  - Admin-Modus verlassen
