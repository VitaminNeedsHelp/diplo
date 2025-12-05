import tkinter as tk
from tkinter import ttk, messagebox


class SettingsScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding=10)

        ttk.Label(self, text="Einstellungen", font=controller.font_title).pack(anchor="n", pady=(10, 10))

        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, pady=(5, 5))

        # Vollbild
        self.var_fullscreen = tk.BooleanVar(value=False)
        chk = ttk.Checkbutton(frm, text="Vollbildmodus", variable=self.var_fullscreen)
        chk.pack(anchor="w", pady=(5, 5))

        # Schriftgröße
        frm_font = ttk.Frame(frm)
        frm_font.pack(anchor="w", pady=(5, 5))
        ttk.Label(frm_font, text="Basis-Schriftgröße:", font=controller.font_normal).pack(side="left")
        self.var_font_size = tk.IntVar(value=controller.base_font_size)
        self.spn_font = tk.Spinbox(frm_font, from_=10, to=40, textvariable=self.var_font_size,
                                   width=5, bg=controller.entry_bg, fg=controller.entry_fg)
        self.spn_font.pack(side="left", padx=(5, 0))

        # Admin logout
        self.btn_logout_admin = tk.Button(frm, text="Admin-Modus verlassen",
                                          font=controller.font_small,
                                          bg=controller.button_bg, fg=controller.button_fg,
                                          command=self.on_logout_admin)
        self.btn_logout_admin.pack(anchor="w", pady=(10, 0))

        # Footer buttons
        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill="x", pady=(10, 10))

        btn_back = tk.Button(frm_buttons, text="Zurück", font=controller.font_normal,
                             bg=controller.button_bg, fg=controller.button_fg,
                             command=lambda: controller.show_frame("HomeScreen"))
        btn_back.pack(side="left", expand=True, fill="x", padx=5)

        btn_save = tk.Button(frm_buttons, text="Speichern", font=controller.font_normal,
                             bg=controller.button_bg, fg=controller.button_fg,
                             command=self.on_save)
        btn_save.pack(side="left", expand=True, fill="x", padx=5)

    def on_show(self):
        s = getattr(self.controller, "settings", {})
        self.var_fullscreen.set(bool(s.get("fullscreen", False)))
        self.var_font_size.set(int(s.get("font_size", self.controller.base_font_size)))

        if getattr(self.controller, "is_admin", False):
            self.btn_logout_admin.config(state="normal")
        else:
            self.btn_logout_admin.config(state="disabled")

    def on_save(self):
        try:
            fs = bool(self.var_fullscreen.get())
        except Exception:
            fs = False
        try:
            font_size = int(self.var_font_size.get())
        except Exception:
            font_size = int(self.controller.base_font_size)

        self.controller.settings["fullscreen"] = fs
        self.controller.settings["font_size"] = font_size

        # persist
        try:
            self.controller.save_settings()
        except Exception:
            pass

        # apply fullscreen immediately
        try:
            self.controller.set_fullscreen(fs)
        except Exception:
            pass

        messagebox.showinfo("Gespeichert", "Einstellungen wurden gespeichert.")

    def on_logout_admin(self):
        if getattr(self.controller, "is_admin", False):
            self.controller.logout_admin()
            self.btn_logout_admin.config(state="disabled")
