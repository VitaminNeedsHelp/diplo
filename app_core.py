#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# Konfig
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    DEFAULT_SETTINGS,
    PRIMARY_BG,
    PRIMARY_FG,
    ADMIN_PASSWORD
)

# Data Store
import data_store as ds

# Optionaler Settings-Store
try:
    from settings_store import load_settings, save_settings
    SETTINGS_STORE_AVAILABLE = True
except Exception:
    SETTINGS_STORE_AVAILABLE = False

    def load_settings():
        return DEFAULT_SETTINGS.copy()

    def save_settings(settings):
        pass

# Screens
from screens_home import HomeScreen
from screens_settings import SettingsScreen
from screens_editor import TutorialEditorScreen
from screens_viewer import TutorialViewerScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # ---------------- Settings ----------------
        self.settings = load_settings() if SETTINGS_STORE_AVAILABLE else DEFAULT_SETTINGS.copy()

        # ---------------- Tutorials ----------------
        self.tutorials_meta = ds.scan_tutorials()
        self.current_tutorial_id = None

        # ---------------- Admin ----------------
        self.is_admin = False

        # ---------------- Fenster ----------------
        self.title("Tutorial-Anzeige")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(360, 640)

        if self.settings.get("fullscreen", False):
            try:
                self.attributes("-fullscreen", True)
            except Exception:
                pass

        # ---------------- Fonts ----------------
        self.base_font_size = int(self.settings.get("font_size", 16))
        self.font_title = ("Sans", int(self.base_font_size * 1.6), "bold")
        self.font_normal = ("Sans", self.base_font_size)
        self.font_small = ("Sans", max(10, int(self.base_font_size * 0.8)))

        # ---------------- Farben ----------------
        self.PRIMARY_BG = PRIMARY_BG
        self.PRIMARY_FG = PRIMARY_FG

        # ---------------- ttk Style (modern & flach) ----------------
        style = ttk.Style(self)
        style.theme_use("clam")

        self.configure(bg=self.PRIMARY_BG)

        style.configure(
            "TFrame",
            background=self.PRIMARY_BG
        )

        style.configure(
            "TLabel",
            background=self.PRIMARY_BG,
            foreground=self.PRIMARY_FG,
            font=self.font_normal
        )

        style.configure(
            "TButton",
            font=self.font_normal,
            padding=(12, 10),
            background=self.PRIMARY_BG,
            foreground=self.PRIMARY_FG,
            borderwidth=0
        )

        # ---------------- Eingabefelder ----------------
        self.entry_bg = "#FFFFFF"
        self.entry_fg = "#000000"

        self.text_bg = "#FFFFFF"
        self.text_fg = "#000000"

        self.listbox_bg = "#FFFFFF"
        self.listbox_fg = "#000000"

        # ---------------- Button Farben ----------------
        self.button_bg = self.PRIMARY_BG
        self.button_fg = self.PRIMARY_FG

        # 🔥 ZENTRALER MODERNER BUTTON-STYLE 🔥
        self.flat_button_cfg = {
            "font": self.font_normal,
            "bg": self.PRIMARY_BG,
            "fg": self.PRIMARY_FG,
            "activebackground": "#5068ff",
            "activeforeground": "#ffffff",
            "bd": 0,
            "highlightthickness": 0,
            "relief": "flat",
            "cursor": "hand2"
        }

        # ---------------- Screen Container ----------------
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for ScreenClass in (
            HomeScreen,
            SettingsScreen,
            TutorialEditorScreen,
            TutorialViewerScreen
        ):
            frame = ScreenClass(parent=container, controller=self)
            self.frames[ScreenClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start
        self.show_frame("HomeScreen")

    # ---------------- Navigation ----------------
    def show_frame(self, name: str):
        frame = self.frames.get(name)
        if not frame:
            return
        if hasattr(frame, "on_show"):
            try:
                frame.on_show()
            except Exception as e:
                print(f"[App] Fehler in {name}.on_show(): {e}")
                raise
        frame.tkraise()

    # ---------------- Tutorials ----------------
    def refresh_tutorials(self):
        self.tutorials_meta = ds.scan_tutorials()

    def create_new_tutorial(self, kind="tutorial", first_page_type="content"):
        if not self.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials anlegen.")
            return

        name = simpledialog.askstring("Name", "Name des Tutorials:")
        if not name:
            return

        meta = ds.create_tutorial(
            name=name,
            kind=kind,
            first_page_type=first_page_type
        )

        self.refresh_tutorials()
        self.current_tutorial_id = str(meta["id"])
        self.show_frame("TutorialEditorScreen")

    def select_tutorial_by_index(self, idx: int):
        if 0 <= idx < len(self.tutorials_meta):
            self.current_tutorial_id = str(self.tutorials_meta[idx]["id"])
            return True
        return False

    def get_current_tutorial(self):
        if not self.current_tutorial_id:
            return None
        return ds.read_tutorial_data(self.current_tutorial_id)

    # Alias (defensiv)
    def get_current(self):
        return self.get_current_tutorial()

    def save_current_tutorial(self, data: dict):
        tid = data.get("id") or self.current_tutorial_id
        if not tid:
            return
        ds.write_tutorial_data(tid, data)
        self.refresh_tutorials()

    def delete_tutorial_at_index(self, index: int):
        if not self.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials löschen.")
            return False

        if not (0 <= index < len(self.tutorials_meta)):
            return False

        tid = self.tutorials_meta[index]["id"]
        name = self.tutorials_meta[index].get("name", tid)

        if not messagebox.askyesno("Löschen", f"Soll '{name}' wirklich gelöscht werden?"):
            return False

        ds.delete_tutorial(tid)
        self.refresh_tutorials()

        if self.current_tutorial_id == tid:
            self.current_tutorial_id = None

        return True

    # ---------------- Admin ----------------
    def prompt_admin_login(self, parent_window=None):
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
            if "HomeScreen" in self.frames:
                self.frames["HomeScreen"].update_admin_ui()
        else:
            messagebox.showerror("Fehler", "Falsches Passwort.")

    def logout_admin(self):
        self.is_admin = False
        messagebox.showinfo("Admin", "Admin-Modus beendet.")
        if "HomeScreen" in self.frames:
            self.frames["HomeScreen"].update_admin_ui()

    # ---------------- Settings ----------------
    def set_fullscreen(self, enabled: bool):
        self.settings["fullscreen"] = bool(enabled)
        try:
            self.attributes("-fullscreen", enabled)
        except Exception:
            pass
        self.save_settings()

    def save_settings(self):
        try:
            save_settings(self.settings)
        except Exception:
            pass

    # ---------------- Debug ----------------
    def tutorial_meta_list(self):
        return [(m.get("id"), m.get("name"), m.get("kind")) for m in self.tutorials_meta]
