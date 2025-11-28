import time
import tkinter as tk
from tkinter import ttk, messagebox


class HomeScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(padding=10)

        # Geheim-Trigger-Variablen (für unsichtbaren Admin-Button)
        self._secret_clicks = 0
        self._last_click_time = 0

        # Titel (klickbar für Admin-Login)
        self.lbl_title = ttk.Label(self, text="Tutorial-Home", font=controller.font_title)
        self.lbl_title.pack(anchor="n", pady=(10, 10))
        self.lbl_title.bind("<Button-1>", self._on_secret_click)

        # Kleiner Hinweis, wenn Admin aktiv
        self.lbl_admin_indicator = ttk.Label(self, text="", font=controller.font_small, foreground="red")
        self.lbl_admin_indicator.pack(anchor="n")

        frm_list = ttk.Frame(self)
        frm_list.pack(fill="both", expand=True, pady=(5, 5))

        lbl_list = ttk.Label(frm_list, text="Verfügbare Tutorials:", font=controller.font_normal)
        lbl_list.pack(anchor="w")

        self.listbox = tk.Listbox(
            frm_list,
            font=controller.font_normal,
            height=10,
            bg=controller.listbox_bg,
            fg=controller.listbox_fg,
            selectbackground="#8888ff"
        )
        self.listbox.pack(fill="both", expand=True, pady=(5, 5))

        # 🔹 Doppelklick auf ein Tutorial -> Viewer öffnen
        self.listbox.bind("<Double-Button-1>", self.on_list_double_click)

        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill="x", pady=(10, 10))

        # Buttons merken, damit wir sie je nach Admin-Status aktivieren/deaktivieren können
        self.btn_new = tk.Button(
            frm_buttons, text="Neues Tutorial",
            font=controller.font_normal,
            command=self.on_new
        )
        self.btn_new.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_edit = tk.Button(
            frm_buttons, text="Tutorial bearbeiten",
            font=controller.font_normal,
            command=self.on_edit
        )
        self.btn_edit.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_delete = tk.Button(
            frm_buttons, text="Tutorial löschen",
            font=controller.font_normal,
            command=self.on_delete
        )
        self.btn_delete.pack(side="left", expand=True, fill="x", padx=5)

        """self.btn_view = tk.Button(
            frm_buttons, text="Tutorial anzeigen",
            font=controller.font_normal,
            command=self.on_view
        )
        self.btn_view.pack(side="left", expand=True, fill="x", padx=5)"""

        # Einstellungen (Logout ist jetzt dort)
        self.btn_settings = tk.Button(
            self, text="Einstellungen",
            font=controller.font_normal,
            command=lambda: controller.show_frame("SettingsScreen")
        )
        self.btn_settings.pack(fill="x", pady=(5, 0))

    # --- Lifecycle ---

    def on_show(self):
        # Liste aktualisieren
        self.listbox.delete(0, tk.END)
        for t in self.controller.tutorials:
            name = t.get("name", "Unbenannt")
            self.listbox.insert(tk.END, name)

        # Admin-UI aktualisieren
        self.update_admin_ui()

    # --- Admin UI ---

    def update_admin_ui(self):
        if self.controller.is_admin:
            self.btn_new.config(state="normal")
            self.btn_edit.config(state="normal")
            self.btn_delete.config(state="normal")
            self.lbl_admin_indicator.config(text="ADMIN-MODUS AKTIV")
        else:
            self.btn_new.config(state="disabled")
            self.btn_edit.config(state="disabled")
            self.btn_delete.config(state="disabled")
            self.lbl_admin_indicator.config(text="")

    # --- Unsichtbarer Admin-Trigger ---

    def _on_secret_click(self, event):
        """
        Wird auf den Titel geklickt.
        Wenn z.B. 5 Klicks innerhalb von 5 Sekunden erfolgt sind -> Admin-Login.
        """
        now = time.time()
        if now - self._last_click_time > 5:
            # Timeout -> Zähler zurücksetzen
            self._secret_clicks = 0

        self._secret_clicks += 1
        self._last_click_time = now

        if self._secret_clicks >= 5:
            self._secret_clicks = 0
            # Admin-Login anstoßen
            self.controller.prompt_admin_login(parent_window=self)

    # --- Buttons / Aktionen ---

    def get_selected_index(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        return sel[0]

    def on_new(self):
        if not self.controller.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials anlegen.")
            return
        self.controller.create_new_tutorial()

    def on_edit(self):
        if not self.controller.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials bearbeiten.")
            return
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Hinweis", "Bitte zuerst ein Tutorial in der Liste auswählen.")
            return
        self.controller.select_tutorial_index(idx)
        self.controller.show_frame("TutorialEditorScreen")

    def on_delete(self):
        if not self.controller.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials löschen.")
            return
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Hinweis", "Bitte zuerst ein Tutorial in der Liste auswählen.")
            return
        name = self.controller.tutorials[idx].get("name", "dieses Tutorial")
        if not messagebox.askyesno("Löschen", f"Soll '{name}' wirklich gelöscht werden?"):
            return
        if self.controller.delete_tutorial_at_index(idx):
            self.on_show()

    def on_view(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Hinweis", "Bitte zuerst ein Tutorial in der Liste auswählen.")
            return
        self.controller.select_tutorial_index(idx)
        self.controller.show_frame("TutorialViewerScreen")

    def on_list_double_click(self, event):
        """Doppelklick auf ein Tutorial in der Liste -> Viewer öffnen (nur Anzeige)."""
        idx = self.get_selected_index()
        if idx is None:
            return
        self.controller.select_tutorial_index(idx)
        self.controller.show_frame("TutorialViewerScreen")
