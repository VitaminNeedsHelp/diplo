import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from config import WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_SETTINGS, ADMIN_PASSWORD
from data_store import load_data, save_data, create_empty_tutorial

from screens_home import HomeScreen
from screens_settings import SettingsScreen
from screens_editor import TutorialEditorScreen
from screens_viewer import TutorialViewerScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # ------------------------------
        # FARBTHEME: Ultramarinblau + Weiß
        # ------------------------------
        PRIMARY_BG = "#4366E6"   # Ultramarinblau
        PRIMARY_FG = "#FFFFFF"   # Weiß

        style = ttk.Style(self)

        self.configure(bg=PRIMARY_BG)
        style.configure(".", background=PRIMARY_BG, foreground=PRIMARY_FG)


        style.configure("TLabel", background=PRIMARY_BG, foreground=PRIMARY_FG)

        style.configure("TButton", background=PRIMARY_BG, foreground=PRIMARY_FG)

        style.configure("TFrame", background=PRIMARY_BG)

        self.listbox_bg = "white"
        self.listbox_fg = "black"

        self.text_bg = "white"
        self.text_fg = "black"


        self.data = load_data()
        self.tutorials = self.data.get("tutorials", [])
        self.settings = self.data.get("settings", DEFAULT_SETTINGS.copy())
        self.current_tutorial_index = None

        # 👮‍♂️ Admin-Flag (nur im RAM)
        self.is_admin = False

        self.title("Tutorial-Anzeige")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(360, 640)

        if self.settings.get("fullscreen", False):
            self.attributes("-fullscreen", True)

        self.base_font_size = self.settings.get("font_size", 16)
        self.font_title = ("Sans", int(self.base_font_size * 1.6), "bold")
        self.font_normal = ("Sans", self.base_font_size)
        self.font_small = ("Sans", max(10, int(self.base_font_size * 0.8)))

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for ScreenClass in (HomeScreen, SettingsScreen, TutorialEditorScreen, TutorialViewerScreen):
            frame = ScreenClass(parent=container, controller=self)
            self.frames[ScreenClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomeScreen")

    # --- Navigation ---

    def show_frame(self, name: str):
        frame = self.frames[name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

    # --- Settings / Speichern ---

    def set_fullscreen(self, enabled: bool):
        self.settings["fullscreen"] = enabled
        self.attributes("-fullscreen", enabled)
        self.save_all()

    def save_all(self):
        self.data["settings"] = self.settings
        self.data["tutorials"] = self.tutorials
        save_data(self.data)

    # --- Tutorials (mit Admin-Prüfung) ---

    def create_new_tutorial(self):
        if not self.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials anlegen.")
            return
        t = create_empty_tutorial()
        self.tutorials.append(t)
        self.current_tutorial_index = len(self.tutorials) - 1
        self.save_all()
        self.show_frame("TutorialEditorScreen")

    def select_tutorial_index(self, index: int):
        if 0 <= index < len(self.tutorials):
            self.current_tutorial_index = index
            return True
        return False

    def get_current_tutorial(self):
        if self.current_tutorial_index is None:
            return None
        if not (0 <= self.current_tutorial_index < len(self.tutorials)):
            return None
        return self.tutorials[self.current_tutorial_index]

    def delete_tutorial_at_index(self, index: int):
        if not self.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials löschen.")
            return False
        if not (0 <= index < len(self.tutorials)):
            return False
        del self.tutorials[index]
        # Index korrigieren
        if self.current_tutorial_index is not None:
            if self.current_tutorial_index >= len(self.tutorials):
                self.current_tutorial_index = len(self.tutorials) - 1
            if len(self.tutorials) == 0:
                self.current_tutorial_index = None
        self.save_all()
        return True

    # --- Admin-Modus ---

    def prompt_admin_login(self, parent_window=None):
        """
        Öffnet ein Passwort-Dialogfenster.
        Wird von einem 'unsichtbaren' Trigger aufgerufen (z.B. mehrfacher Klick auf Titel).
        """
        pw = simpledialog.askstring(
            "Admin-Login",
            "Bitte Admin-Passwort eingeben:",
            show="*",
            parent=parent_window or self
        )
        if pw is None:
            return  # Abgebrochen

        if pw == ADMIN_PASSWORD:
            self.is_admin = True
            messagebox.showinfo("Admin", "Admin-Modus aktiviert.")
            # Home-Screen aktualisieren, damit Buttons freigeschaltet werden
            if "HomeScreen" in self.frames:
                self.frames["HomeScreen"].update_admin_ui()
        else:
            messagebox.showerror("Fehler", "Falsches Passwort.")

    def logout_admin(self):
        self.is_admin = False
        messagebox.showinfo("Admin", "Admin-Modus beendet.")
        if "HomeScreen" in self.frames:
            self.frames["HomeScreen"].update_admin_ui()
