#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# konfig / pfad-werte
from config import WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_SETTINGS, PRIMARY_BG, PRIMARY_FG, ADMIN_PASSWORD, TUTORIALS_DIR

# data_store (neues filesystem-basiertes backend)
import data_store as ds

# optional: settings in separater Datei (falls vorhanden)
try:
    from settings_store import load_settings, save_settings
    SETTINGS_STORE_AVAILABLE = True
except Exception:
    SETTINGS_STORE_AVAILABLE = False
    def load_settings():  # fallback
        return DEFAULT_SETTINGS.copy()
    def save_settings(s):
        # fallback: no-op
        return

# Screens (werden erwartet, vorhanden zu sein)
from screens_home import HomeScreen
from screens_settings import SettingsScreen
from screens_editor import TutorialEditorScreen
from screens_viewer import TutorialViewerScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # ---- Settings laden (separater settings-store oder Defaults) ----
        self.settings = load_settings() if SETTINGS_STORE_AVAILABLE else DEFAULT_SETTINGS.copy()

        # ---- Tutorials Meta: immer live aus filesystem scannen ----
        self.tutorials_meta = ds.scan_tutorials()

        # aktives tutorial id (string) oder None
        self.current_tutorial_id = None

        # Admin-Flag
        self.is_admin = False

        # Fenster
        self.title("Tutorial-Anzeige")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(360, 640)

        if self.settings.get("fullscreen", False):
            try:
                self.attributes("-fullscreen", True)
            except Exception:
                pass

        # Fonts (basierend auf settings)
        self.base_font_size = int(self.settings.get("font_size", DEFAULT_SETTINGS.get("font_size", 16)))
        self.font_title = ("Sans", int(self.base_font_size * 1.6), "bold")
        self.font_normal = ("Sans", self.base_font_size)
        self.font_small = ("Sans", max(10, int(self.base_font_size * 0.8)))

        # Theme / Farben
        self.PRIMARY_BG = PRIMARY_BG
        self.PRIMARY_FG = PRIMARY_FG

        style = ttk.Style(self)
        self.configure(bg=self.PRIMARY_BG)
        style.configure(".", background=self.PRIMARY_BG, foreground=self.PRIMARY_FG)
        style.configure("TLabel", background=self.PRIMARY_BG, foreground=self.PRIMARY_FG)
        style.configure("TFrame", background=self.PRIMARY_BG)
        style.configure("TButton", background=self.PRIMARY_BG, foreground=self.PRIMARY_FG)

        # Eingabefeld-Farben (explizit, damit ttk-Theme sie nicht überschreibt)
        self.entry_bg = "#FFFFFF"
        self.entry_fg = "#000000"

        self.text_bg = "#FFFFFF"
        self.text_fg = "#000000"

        self.listbox_bg = "#FFFFFF"
        self.listbox_fg = "#000000"

        self.button_bg = self.PRIMARY_BG
        self.button_fg = self.PRIMARY_FG

        # Container für Screens
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Screens initialisieren und im Dict halten
        self.frames = {}
        for ScreenClass in (HomeScreen, SettingsScreen, TutorialEditorScreen, TutorialViewerScreen):
            frame = ScreenClass(parent=container, controller=self)
            self.frames[ScreenClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Startscreen anzeigen
        self.show_frame("HomeScreen")

    # ---------------- Navigation / Screen-Management ----------------
    def show_frame(self, name: str):
        """Zeigt Screen mit Namen an und ruft on_show falls vorhanden."""
        frame = self.frames.get(name)
        if not frame:
            return
        if hasattr(frame, "on_show"):
            try:
                frame.on_show()
            except Exception as e:
                # Fehler im on_show nicht komplett unterdrücken — zeige Meldung und re-raise evtl.
                print(f"[App] Fehler in {name}.on_show():", e)
                raise
        frame.tkraise()

    # ---------------- Tutorials (Filesystem-basiert) ----------------
    def refresh_tutorials(self):
        """Scannt tutorials/ neu und aktualisiert meta-liste."""
        self.tutorials_meta = ds.scan_tutorials()

    def create_new_tutorial(self, name="Neues Tutorial"):
        """Legt ein neues Tutorial an (nur Admins)."""
        if not self.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials anlegen.")
            return
        meta = ds.create_tutorial(name=name)
        # Refresh metas und setze neues Tutorial als aktuell
        self.refresh_tutorials()
        self.current_tutorial_id = meta["id"]
        # zeige Editor
        self.show_frame("TutorialEditorScreen")

    def select_tutorial_by_index(self, idx: int):
        """
        Wählt das Tutorial per Index in tutorials_meta aus.
        Gibt True zurück bei Erfolg.
        """
        if 0 <= idx < len(self.tutorials_meta):
            self.current_tutorial_id = str(self.tutorials_meta[idx]["id"])
            return True
        return False

    def get_current_tutorial(self):
        """
        Liest und gibt das per-tutorial data dict zurück.
        Falls kein Tutorial selektiert ist, None.
        """
        if not self.current_tutorial_id:
            return None
        data = ds.read_tutorial_data(self.current_tutorial_id)
        return data

    def save_current_tutorial(self, data: dict):
        """
        Schreibt das tutorial-data dict in die per-tutorial data.json.
        Aktualisiert die Meta-Liste und ggf. den Namen in metas.
        """
        tid = data.get("id") or self.current_tutorial_id
        if not tid:
            return
        ds.write_tutorial_data(tid, data)
        # Refresh metas (so Name/Folder werden aktuell)
        self.refresh_tutorials()

    def delete_tutorial_at_index(self, index: int):
        """Löscht Tutorial-Ordner und aktualisiert metas (nur Admins)."""
        if not self.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials löschen.")
            return False
        if not (0 <= index < len(self.tutorials_meta)):
            return False
        tid = self.tutorials_meta[index]["id"]
        # Bestätigung
        name = self.tutorials_meta[index].get("name", tid)
        if not messagebox.askyesno("Löschen", f"Soll '{name}' wirklich gelöscht werden?"):
            return False
        ds.delete_tutorial(tid)
        self.refresh_tutorials()
        # falls gelöschtes Tutorial aktuell war, clear selection
        if self.current_tutorial_id == tid:
            self.current_tutorial_id = None
        return True

    # ---------------- Admin ----------------
    def prompt_admin_login(self, parent_window=None):
        """Fragt Passwort ab und setzt is_admin True falls korrekt."""
        pw = simpledialog.askstring(
            "Admin-Login",
            "Bitte Admin-Passwort eingeben:",
            show="*",
            parent=parent_window or self
        )
        if pw is None:
            return
        if pw == ADMIN_PASSWORD:
            self.is_admin = True
            messagebox.showinfo("Admin", "Admin-Modus aktiviert.")
            # HomeScreen UI updaten falls vorhanden
            if "HomeScreen" in self.frames:
                try:
                    self.frames["HomeScreen"].update_admin_ui()
                except Exception:
                    pass
        else:
            messagebox.showerror("Fehler", "Falsches Passwort.")

    def logout_admin(self):
        self.is_admin = False
        messagebox.showinfo("Admin", "Admin-Modus beendet.")
        if "HomeScreen" in self.frames:
            try:
                self.frames["HomeScreen"].update_admin_ui()
            except Exception:
                pass

    # ---------------- Settings (separates file via settings_store) ----------------
    def set_fullscreen(self, enabled: bool):
        """Setzt Vollbild-Flag in memory und auf Fenster."""
        self.settings["fullscreen"] = bool(enabled)
        try:
            self.attributes("-fullscreen", enabled)
        except Exception:
            pass
        # persist settings if store available
        self.save_settings()

    def save_settings(self):
        """Speichert Einstellungen via settings_store (wenn vorhanden)."""
        try:
            save_settings(self.settings)
        except Exception:
            # fallback: ignore save error
            pass

    # ---------------- Utility / Debug ----------------
    def tutorial_meta_list(self):
        """Hilfsfunktion: liefert Liste von (id,name) für Debug/Views."""
        return [(m.get("id"), m.get("name")) for m in self.tutorials_meta]
