import time
import os
import tkinter as tk
from tkinter import ttk, messagebox

import data_store as ds
from image_utils import load_image_for_tk


class HomeScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding=10)

        # Secret click (Admin)
        self._secret_clicks = 0
        self._last_click_time = 0

        # Auswahl-Handling für Cards
        self.selected_index = None
        self._selected_card = None

        # Bild-Referenzen halten (wichtig!)
        self._preview_imgs = []

        # Titel
        self.lbl_title = tk.Label(
            self,
            text="Tutorial-Home",
            font=controller.font_title,
            bg=controller.PRIMARY_BG,
            fg=controller.PRIMARY_FG
        )
        self.lbl_title.pack(anchor="n", pady=(10, 10))
        self.lbl_title.bind("<Button-1>", self._on_secret_click)

        # Admin indicator
        self.lbl_admin_indicator = ttk.Label(
            self,
            text="",
            font=controller.font_small,
            foreground="red"
        )
        self.lbl_admin_indicator.pack(anchor="n")

        # ---------- Scrollbereich (Cards) ----------
        self.canvas = tk.Canvas(
            self,
            bg=controller.PRIMARY_BG,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, pady=(5, 5))

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )
        self.scrollbar.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.cards_frame = tk.Frame(
            self.canvas,
            bg=controller.PRIMARY_BG
        )
        self.canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")

        self.cards_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # ---------- Buttons ----------
        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill="x", padx=5, pady=(10, 5))

        self.btn_new = tk.Button(
            frm_buttons,
            text="Neues Tutorial",
            font=controller.font_normal,
            bg=controller.button_bg,
            fg=controller.button_fg,
            command=self.on_new
        )
        self.btn_new.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_edit = tk.Button(
            frm_buttons,
            text="Tutorial bearbeiten",
            font=controller.font_normal,
            bg=controller.button_bg,
            fg=controller.button_fg,
            command=self.on_edit
        )
        self.btn_edit.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_delete = tk.Button(
            frm_buttons,
            text="Tutorial löschen",
            font=controller.font_normal,
            bg=controller.button_bg,
            fg=controller.button_fg,
            command=self.on_delete
        )
        self.btn_delete.pack(side="left", expand=True, fill="x", padx=5)

        # Settings
        frm_settings = ttk.Frame(self)
        frm_settings.pack(fill="x", padx=10, pady=(0, 10))

        self.btn_settings = tk.Button(
            frm_settings,
            text="Einstellungen",
            font=controller.font_normal,
            bg=controller.button_bg,
            fg=controller.button_fg,
            command=lambda: controller.show_frame("SettingsScreen")
        )
        self.btn_settings.pack(fill="x")

    # ---------------- Lifecycle ----------------
    def on_show(self):
        self.controller.refresh_tutorials()
        self._build_cards()
        self.update_admin_ui()

    # ---------------- Cards ----------------
    def _build_cards(self):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        self._preview_imgs.clear()
        self.selected_index = None
        self._selected_card = None

        for idx, meta in enumerate(self.controller.tutorials_meta):
            self._create_card(idx, meta)

    def _create_card(self, index, meta):
        card = tk.Frame(
            self.cards_frame,
            bg="#4366E6",
            padx=12,
            pady=10
        )
        card.pack(fill="x", padx=8, pady=6)

        # Icon
        icon_lbl = tk.Label(card, bg="#4366E6")
        icon_lbl.pack(side="left", padx=(0, 12))

        img = self._load_preview_icon(meta)
        if img:
            icon_lbl.config(image=img)
            self._preview_imgs.append(img)
        else:
            icon_lbl.config(text="📄", font=("Sans", 24))

        # Text
        text_frame = tk.Frame(card, bg="#4366E6")
        text_frame.pack(side="left", fill="x", expand=True)

        name = meta.get("name", "Unbenannt")
        kind = meta.get("kind", "tutorial")

        tk.Label(
            text_frame,
            text=name,
            font=self.controller.font_normal,
            bg="#4366E6",
            fg="#FFFFFF",
            anchor="w"
        ).pack(fill="x")

        if kind == "quiz":
            tk.Label(
                text_frame,
                text="Quiz",
                font=self.controller.font_small,
                bg="#4366E6",
                fg="#FFFFFF",
                anchor="w"
            ).pack(fill="x")

        # Klick-Handling (Auswahl + Öffnen per Doppelklick-Ersatz)
        def on_click(event):
            self._select_card(index, card)

        def on_double_click(event):
            self._select_card(index, card)
            self.on_view()

        card.bind("<Button-1>", on_click)
        card.bind("<Double-Button-1>", on_double_click)
        for child in card.winfo_children():
            child.bind("<Button-1>", on_click)
            child.bind("<Double-Button-1>", on_double_click)

    def _select_card(self, index, card):
        # alte Auswahl zurücksetzen
        if self._selected_card:
            self._selected_card.config(bg="#FFFFFF")

        self.selected_index = index
        self._selected_card = card
        card.config(bg="#E8ECFF")  # dezente Auswahlfarbe

    def _load_preview_icon(self, meta):
        tid = meta.get("id")
        if not tid:
            return None

        data = ds.read_tutorial_data(tid)
        if not data:
            return None

        pages = data.get("pages", [])
        if not pages:
            return None

        img_name = pages[0].get("image")
        if not img_name:
            return None

        img_dir = ds.tutorial_images_dir(tid)
        img_path = os.path.join(img_dir, img_name)

        return load_image_for_tk(img_path, 64, 64)

    # ---------------- Admin UI ----------------
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

    # ---------------- Admin Secret ----------------
    def _on_secret_click(self, event):
        now = time.time()
        if now - self._last_click_time > 5:
            self._secret_clicks = 0
        self._secret_clicks += 1
        self._last_click_time = now

        if self._secret_clicks >= 5:
            self._secret_clicks = 0
            self.controller.prompt_admin_login(parent_window=self)

    # ---------------- Helpers ----------------
    def get_selected_index(self):
        return self.selected_index

    # ---------------- Actions ----------------
    def on_new(self):
        if not self.controller.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials anlegen.")
            return
        self._open_type_dialog()

    def on_view(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Hinweis", "Bitte zuerst ein Tutorial auswählen.")
            return
        if self.controller.select_tutorial_by_index(idx):
            self.controller.show_frame("TutorialViewerScreen")

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
            self.on_show()

    # ---------- Dialoge (UNVERÄNDERT von deinem Stand) ----------
    def _open_type_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("Tutorial-Typ wählen")
        dlg.transient(self)
        dlg.grab_set()
        dlg.resizable(False, False)

        dlg.configure(bg=self.controller.PRIMARY_BG)

        tk.Label(
            dlg,
            text="Was möchtest du erstellen?",
            font=self.controller.font_normal,
            bg=self.controller.PRIMARY_BG,
            fg=self.controller.PRIMARY_FG
        ).pack(padx=20, pady=(15, 10))

        def choose(kind):
            dlg.destroy()
            self._handle_kind_choice(kind)

        btn_cfg = {
            "width": 35,
            "font": self.controller.font_normal,
            "bg": self.controller.button_bg,
            "fg": self.controller.button_fg,
            "activebackground": self.controller.button_bg,
            "activeforeground": self.controller.button_fg
        }

        tk.Button(dlg, text="📘 Reines Tutorial (nur Inhalt)", command=lambda: choose("tutorial"), **btn_cfg)\
            .pack(padx=20, pady=5)
        tk.Button(dlg, text="🧠 Reines Quiz", command=lambda: choose("quiz"), **btn_cfg)\
            .pack(padx=20, pady=5)
        tk.Button(dlg, text="🔀 Gemischt (Inhalt + Quiz)", command=lambda: choose("gemischt"), **btn_cfg)\
            .pack(padx=20, pady=(5, 15))

        dlg.wait_window()

    def _handle_kind_choice(self, kind):
        if kind == "tutorial":
            self.controller.create_new_tutorial(kind="tutorial", first_page_type="content")
            return
        if kind == "quiz":
            self.controller.create_new_tutorial(kind="quiz", first_page_type="quiz")
            return
        self._open_first_page_dialog()

    def _open_first_page_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("Erste Seite")
        dlg.transient(self)
        dlg.grab_set()
        dlg.resizable(False, False)

        dlg.configure(bg=self.controller.PRIMARY_BG)

        tk.Label(
            dlg,
            text="Womit soll das Tutorial beginnen?",
            font=self.controller.font_normal,
            bg=self.controller.PRIMARY_BG,
            fg=self.controller.PRIMARY_FG
        ).pack(padx=20, pady=(15, 10))

        btn_cfg = {
            "width": 30,
            "font": self.controller.font_normal,
            "bg": self.controller.button_bg,
            "fg": self.controller.button_fg,
            "activebackground": self.controller.button_bg,
            "activeforeground": self.controller.button_fg
        }

        def choose(first):
            dlg.destroy()
            self.controller.create_new_tutorial(kind="gemischt", first_page_type=first)

        tk.Button(dlg, text="📝 Inhalt", command=lambda: choose("content"), **btn_cfg)\
            .pack(padx=20, pady=5)
        tk.Button(dlg, text="🧠 Quiz", command=lambda: choose("quiz"), **btn_cfg)\
            .pack(padx=20, pady=(5, 15))

        dlg.wait_window()
