import time
import tkinter as tk
from tkinter import ttk, messagebox


class HomeScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding=10)

        # Secret click
        self._secret_clicks = 0
        self._last_click_time = 0

        # Titel (sichtbar)
        self.lbl_title = tk.Label(
            self,
            text="Tutorial-Home",
            font=controller.font_title,
            bg=controller.PRIMARY_BG,
            fg=controller.PRIMARY_FG
        )
        self.lbl_title.pack(anchor="n", pady=(10, 10))
        self.lbl_title.bind("<Button-1>", self._on_secret_click)

        # Admin-Indikator
        self.lbl_admin_indicator = ttk.Label(self, text="", font=controller.font_small, foreground="red")
        self.lbl_admin_indicator.pack(anchor="n")

        # List area
        frm_list = ttk.Frame(self)
        frm_list.pack(fill="both", expand=True, pady=(5, 5))

        ttk.Label(frm_list, text="Verfügbare Tutorials:", font=controller.font_normal).pack(anchor="w")

        self.listbox = tk.Listbox(
            frm_list,
            font=controller.font_normal,
            height=10,
            bg=controller.listbox_bg,
            fg=controller.listbox_fg,
            selectbackground="#8897ff"
        )
        self.listbox.pack(fill="both", expand=True, pady=(5, 5))
        self.listbox.bind("<Double-Button-1>", self.on_list_double_click)

        # Buttons
        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill="x", pady=(10, 10))

        self.btn_new = tk.Button(frm_buttons, text="Neues Tutorial",
                                 font=controller.font_normal,
                                 bg=controller.button_bg, fg=controller.button_fg,
                                 command=self.on_new)
        self.btn_new.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_edit = tk.Button(frm_buttons, text="Tutorial bearbeiten",
                                  font=controller.font_normal,
                                  bg=controller.button_bg, fg=controller.button_fg,
                                  command=self.on_edit)
        self.btn_edit.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_delete = tk.Button(frm_buttons, text="Tutorial löschen",
                                    font=controller.font_normal,
                                    bg=controller.button_bg, fg=controller.button_fg,
                                    command=self.on_delete)
        self.btn_delete.pack(side="left", expand=True, fill="x", padx=5)
        
        # Settings
        self.btn_settings = tk.Button(self, text="Einstellungen",
                                      font=controller.font_normal,
                                      bg=controller.button_bg, fg=controller.button_fg,
                                      command=lambda: controller.show_frame("SettingsScreen"))
        self.btn_settings.pack(fill="x", pady=(5, 0))

    def on_show(self):
        # Refresh the list from filesystem
        try:
            self.controller.refresh_tutorials()
        except Exception:
            pass

        self.listbox.delete(0, tk.END)
        metas = getattr(self.controller, "tutorials_meta", []) or []
        for m in metas:
            self.listbox.insert(tk.END, m.get("name", "Unbenannt"))

        self.update_admin_ui()

    def update_admin_ui(self):
        if getattr(self.controller, "is_admin", False):
            self.btn_new.config(state="normal")
            self.btn_edit.config(state="normal")
            self.btn_delete.config(state="normal")
            self.lbl_admin_indicator.config(text="ADMIN-MODUS AKTIV")
        else:
            self.btn_new.config(state="disabled")
            self.btn_edit.config(state="disabled")
            self.btn_delete.config(state="disabled")
            self.lbl_admin_indicator.config(text="")

    def _on_secret_click(self, event):
        now = time.time()
        if now - self._last_click_time > 5:
            self._secret_clicks = 0
        self._secret_clicks += 1
        self._last_click_time = now
        if self._secret_clicks >= 5:
            self._secret_clicks = 0
            self.controller.prompt_admin_login(parent_window=self)

    def get_selected_index(self):
        sel = self.listbox.curselection()
        return sel[0] if sel else None

    def on_new(self):
        if not self.controller.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials anlegen.")
            return
        # optional: ask for name
        self.controller.create_new_tutorial()

    def on_edit(self):
        if not self.controller.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials bearbeiten.")
            return
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Hinweis", "Bitte zuerst ein Tutorial auswählen.")
            return
        if self.controller.select_tutorial_by_index(idx):
            self.controller.show_frame("TutorialEditorScreen")

    def on_delete(self):
        if not self.controller.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials löschen.")
            return
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Hinweis", "Bitte zuerst ein Tutorial auswählen.")
            return
        if self.controller.delete_tutorial_at_index(idx):
            # refresh view
            self.on_show()

    def on_view(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Hinweis", "Bitte zuerst ein Tutorial auswählen.")
            return
        if self.controller.select_tutorial_by_index(idx):
            self.controller.show_frame("TutorialViewerScreen")

    def on_list_double_click(self, event):
        self.on_view()
