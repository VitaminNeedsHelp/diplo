import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from config import IMAGES_DIR


class TutorialEditorScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding=10)

        self.current_page_index = 0

        # Titel
        lbl_title = ttk.Label(self, text="Tutorial bearbeiten", font=controller.font_title)
        lbl_title.pack(anchor="n", pady=(5, 10))

        # Tutorial-Name
        frm_name = ttk.Frame(self)
        frm_name.pack(fill="x", pady=(5, 5))
        ttk.Label(frm_name, text="Tutorial-Titel:", font=controller.font_normal)\
            .pack(side="left")
        self.entry_tutorial_name = ttk.Entry(frm_name, font=controller.font_normal)
        self.entry_tutorial_name.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Seiten-Navigation
        frm_page_nav = ttk.Frame(self)
        frm_page_nav.pack(fill="x", pady=(10, 5))

        self.btn_prev_page = tk.Button(
            frm_page_nav, text="◀ Seite",
            font=controller.font_normal,
            command=self.on_prev_page
        )
        self.btn_prev_page.pack(side="left")

        self.lbl_page_info = ttk.Label(frm_page_nav, text="Seite 1/1", font=controller.font_normal)
        self.lbl_page_info.pack(side="left", expand=True)

        self.btn_next_page = tk.Button(
            frm_page_nav, text="Seite ▶",
            font=controller.font_normal,
            command=self.on_next_page
        )
        self.btn_next_page.pack(side="left")

        btn_add_page = tk.Button(
            self, text="Seite hinzufügen",
            font=controller.font_normal,
            command=self.on_add_page
        )
        btn_add_page.pack(fill="x", pady=(5, 10))

        # Seiten-Inhalt
        frm_content = ttk.Frame(self)
        frm_content.pack(fill="both", expand=True)

        # Seitentitel
        frm_page_title = ttk.Frame(frm_content)
        frm_page_title.pack(fill="x", pady=(5, 5))
        ttk.Label(frm_page_title, text="Seitentitel:", font=controller.font_normal)\
            .pack(side="left")
        self.entry_page_title = ttk.Entry(frm_page_title, font=controller.font_normal)
        self.entry_page_title.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Bildpfad + Button
        frm_image = ttk.Frame(frm_content)
        frm_image.pack(fill="x", pady=(5, 5))
        ttk.Label(frm_image, text="Bild:", font=controller.font_normal)\
            .pack(side="left")
        self.entry_image = ttk.Entry(frm_image, font=controller.font_normal)
        self.entry_image.pack(side="left", fill="x", expand=True, padx=(5, 5))

        btn_pick_image = tk.Button(
            frm_image, text="Auswählen…",
            font=controller.font_small,
            command=self.on_pick_image
        )
        btn_pick_image.pack(side="left")

        # Text
        lbl_text = ttk.Label(frm_content, text="Text:", font=controller.font_normal)
        lbl_text.pack(anchor="w", pady=(5, 0))

        self.text_page = tk.Text(
            frm_content,
            height=15,
            font=controller.font_normal,
            wrap="word",
            bg=controller.text_bg,
            fg=controller.text_fg
        )
        self.text_page.pack(fill="both", expand=True, pady=(2, 5))

        # Buttons unten
        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill="x", pady=(10, 10))

        btn_back = tk.Button(
            frm_buttons, text="Zurück",
            font=controller.font_normal,
            command=self.on_back
        )
        btn_back.pack(side="left", expand=True, fill="x", padx=5)

        btn_save = tk.Button(
            frm_buttons, text="Speichern",
            font=controller.font_normal,
            command=self.on_save
        )
        btn_save.pack(side="left", expand=True, fill="x", padx=5)

    # ---------------- Lifecycle ----------------

    def on_show(self):
        """Wird aufgerufen, wenn der Screen angezeigt wird."""
        # ❗ Nur Admin darf hier hinein
        if not self.controller.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials bearbeiten.")
            self.controller.show_frame("HomeScreen")
            return

        tutorial = self.controller.get_current_tutorial()
        if not tutorial:
            self.controller.show_frame("HomeScreen")
            return

        self.current_page_index = 0
        self.entry_tutorial_name.delete(0, tk.END)
        self.entry_tutorial_name.insert(0, tutorial.get("name", ""))

        self.load_page_into_gui()

    # ---------------- Hilfsfunktionen ----------------

    def save_gui_into_current_page(self):
        """Aktuelle GUI-Felder in die aktuelle Seite des Tutorials schreiben."""
        tutorial = self.controller.get_current_tutorial()
        if not tutorial:
            return
        pages = tutorial.setdefault("pages", [])
        if not pages:
            pages.append({"title": "", "image": "", "text": ""})
        if not (0 <= self.current_page_index < len(pages)):
            return

        page = pages[self.current_page_index]
        page["title"] = self.entry_page_title.get()
        page["image"] = self.entry_image.get()
        page["text"] = self.text_page.get("1.0", tk.END).rstrip("\n")

    def load_page_into_gui(self):
        """Aktuelle Seite aus dem Tutorial in die GUI-Felder laden."""
        tutorial = self.controller.get_current_tutorial()
        if not tutorial:
            return
        pages = tutorial.setdefault("pages", [])
        if not pages:
            pages.append({"title": "", "image": "", "text": ""})
            self.current_page_index = 0
        if self.current_page_index >= len(pages):
            self.current_page_index = len(pages) - 1

        page = pages[self.current_page_index]

        self.entry_page_title.delete(0, tk.END)
        self.entry_page_title.insert(0, page.get("title", ""))

        self.entry_image.delete(0, tk.END)
        self.entry_image.insert(0, page.get("image", ""))

        self.text_page.delete("1.0", tk.END)
        self.text_page.insert("1.0", page.get("text", ""))

        total = len(pages)
        self.lbl_page_info.config(text=f"Seite {self.current_page_index + 1} / {total}")

        if self.current_page_index == 0:
            self.btn_prev_page.config(state="disabled")
        else:
            self.btn_prev_page.config(state="normal")

        if self.current_page_index == total - 1:
            self.btn_next_page.config(state="disabled")
        else:
            self.btn_next_page.config(state="normal")

    # ---------------- Navigation ----------------

    def on_prev_page(self):
        """Eine Seite zurück."""
        self.save_gui_into_current_page()
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.load_page_into_gui()

    def on_next_page(self):
        """Eine Seite vor."""
        self.save_gui_into_current_page()
        tutorial = self.controller.get_current_tutorial()
        if not tutorial:
            return
        pages = tutorial.setdefault("pages", [])
        if self.current_page_index < len(pages) - 1:
            self.current_page_index += 1
            self.load_page_into_gui()

    def on_add_page(self):
        """Neue Seite nach der aktuellen einfügen."""
        self.save_gui_into_current_page()
        tutorial = self.controller.get_current_tutorial()
        if not tutorial:
            return
        pages = tutorial.setdefault("pages", [])
        new_page = {
            "title": f"Seite {len(pages) + 1}",
            "image": "",
            "text": ""
        }
        insert_index = self.current_page_index + 1
        pages.insert(insert_index, new_page)
        self.current_page_index = insert_index
        self.load_page_into_gui()

    # ---------------- Bild auswählen ----------------

    def on_pick_image(self):
        """Dateidialog zum Bild auswählen."""
        filename = filedialog.askopenfilename(
            title="Bild auswählen",
            initialdir=IMAGES_DIR,
            filetypes=[("Bilder", "*.png *.gif *.jpg *.jpeg *.bmp"), ("Alle Dateien", "*.*")]
        )
        if not filename:
            return

        try:
            rel = os.path.relpath(filename, IMAGES_DIR)
            if not rel.startswith(".."):
                self.entry_image.delete(0, tk.END)
                self.entry_image.insert(0, rel)
            else:
                self.entry_image.delete(0, tk.END)
                self.entry_image.insert(0, filename)
        except Exception:
            self.entry_image.delete(0, tk.END)
            self.entry_image.insert(0, filename)

    # ---------------- Buttons unten ----------------

    def on_back(self):
        """Zurück zum Home-Screen (vorher speichern)."""
        self.on_save()
        self.controller.show_frame("HomeScreen")

    def on_save(self):
        """Aktuelle Seite + Tutorial-Titel speichern."""
        tutorial = self.controller.get_current_tutorial()
        if not tutorial:
            return
        self.save_gui_into_current_page()
        tutorial["name"] = self.entry_tutorial_name.get() or "Unbenannt"
        self.controller.save_all()
        messagebox.showinfo("Gespeichert", "Tutorial wurde gespeichert.")
