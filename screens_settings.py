import tkinter as tk
from tkinter import ttk, messagebox


class SettingsScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding=10)

        lbl_title = ttk.Label(self, text="Einstellungen", font=controller.font_title)
        lbl_title.pack(anchor="n", pady=(10, 10))

        frm_content = ttk.Frame(self)
        frm_content.pack(fill="both", expand=True, pady=(5, 5))

        # Vollbild
        self.var_fullscreen = tk.BooleanVar(value=False)
        chk_full = ttk.Checkbutton(
            frm_content, text="Vollbildmodus",
            variable=self.var_fullscreen
        )
        chk_full.pack(anchor="w", pady=(5, 5))

        # Schriftgröße
        frm_font = ttk.Frame(frm_content)
        frm_font.pack(anchor="w", pady=(5, 5))
        ttk.Label(frm_font, text="Basis-Schriftgröße:", font=controller.font_normal)\
            .pack(side="left")

        self.var_font_size = tk.IntVar(value=controller.base_font_size)
        spn_font = tk.Spinbox(frm_font, from_=10, to=40, textvariable=self.var_font_size, width=5)
        spn_font.pack(side="left", padx=(5, 0))

        # 🔹 Admin-Logout-Button
        self.btn_logout_admin = tk.Button(
            frm_content,
            text="Admin-Modus verlassen",
            font=controller.font_small,
            command=self.on_logout_admin
        )
        self.btn_logout_admin.pack(anchor="w", pady=(10, 0))

        # Buttons unten
        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill="x", pady=(10, 10))

        btn_back = tk.Button(
            frm_buttons, text="Zurück",
            font=controller.font_normal,
            command=lambda: controller.show_frame("HomeScreen")
        )
        btn_back.pack(side="left", expand=True, fill="x", padx=5)

        btn_save = tk.Button(
            frm_buttons, text="Speichern",
            font=controller.font_normal,
            command=self.on_save
        )
        btn_save.pack(side="left", expand=True, fill="x", padx=5)

    def on_show(self):
        # aktuelle Settings in GUI schreiben
        s = self.controller.settings
        self.var_fullscreen.set(s.get("fullscreen", False))
        self.var_font_size.set(s.get("font_size", 16))

        # Admin-Logout-Button nur aktiv, wenn gerade Admin
        if self.controller.is_admin:
            self.btn_logout_admin.config(state="normal")
        else:
            self.btn_logout_admin.config(state="disabled")

    def on_save(self):
        self.controller.settings["fullscreen"] = bool(self.var_fullscreen.get())
        self.controller.settings["font_size"] = int(self.var_font_size.get())
        self.controller.save_all()
        self.controller.set_fullscreen(self.controller.settings["fullscreen"])
        messagebox.showinfo("Gespeichert", "Einstellungen wurden gespeichert.\nEinige Änderungen wirken erst nach Neustart.")

    def on_logout_admin(self):
        """Admin-Modus beenden."""
        if self.controller.is_admin:
            self.controller.logout_admin()
            # Button nach Logout deaktivieren
            self.btn_logout_admin.config(state="disabled")