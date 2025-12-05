import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import data_store as ds
from image_utils import load_image_for_tk


class TutorialEditorScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding=8)

        self.current_page_index = 0
        self.tutorial_data = None
        self._preview_img_ref = None

        ttk.Label(self, text="Tutorial bearbeiten", font=controller.font_title).pack(anchor="n", pady=(4, 8))

        # content frame
        self.frm_content = ttk.Frame(self)
        self.frm_content.pack(fill="both", expand=True)

        # Titel
        frm_name = ttk.Frame(self.frm_content)
        frm_name.pack(fill="x", pady=(2, 6))
        ttk.Label(frm_name, text="Tutorial-Titel:", font=controller.font_normal).pack(side="left")
        self.entry_tutorial_name = tk.Entry(frm_name, font=controller.font_normal,
                                            bg=controller.entry_bg, fg=controller.entry_fg)
        self.entry_tutorial_name.pack(side="left", fill="x", expand=True, padx=(6, 0))

        # page nav
        frm_page_nav = ttk.Frame(self.frm_content)
        frm_page_nav.pack(fill="x", pady=(4, 6))
        self.btn_prev_page = tk.Button(frm_page_nav, text="◀ Seite", font=controller.font_normal,
                                       bg=controller.button_bg, fg=controller.button_fg, command=self.on_prev_page)
        self.btn_prev_page.pack(side="left")
        self.lbl_page_info = ttk.Label(frm_page_nav, text="Seite 1/1", font=controller.font_normal)
        self.lbl_page_info.pack(side="left", expand=True, padx=8)
        self.btn_next_page = tk.Button(frm_page_nav, text="Seite ▶", font=controller.font_normal,
                                       bg=controller.button_bg, fg=controller.button_fg, command=self.on_next_page)
        self.btn_next_page.pack(side="left")

        # add page button
        self.btn_add_page = tk.Button(self.frm_content, text="Seite hinzufügen", font=controller.font_normal,
                                     bg=controller.button_bg, fg=controller.button_fg, command=self.on_add_page)
        self.btn_add_page.pack(fill="x", pady=(4, 8))

        # image entry + picker
        self.frm_preview = ttk.Frame(self.frm_content)
        self.frm_preview.pack(fill="x", pady=(2, 6))
        frm_image = ttk.Frame(self.frm_preview)
        frm_image.pack(fill="x")
        ttk.Label(frm_image, text="Bild:", font=controller.font_normal).pack(side="left")
        self.entry_image = tk.Entry(frm_image, font=controller.font_normal,
                                    bg=controller.entry_bg, fg=controller.entry_fg)
        self.entry_image.pack(side="left", fill="x", expand=True, padx=(6, 6))
        btn_pick_image = tk.Button(frm_image, text="Auswählen…", font=controller.font_small,
                                   bg=controller.button_bg, fg=controller.button_fg, command=self.on_pick_image)
        btn_pick_image.pack(side="left")

        # preview holder (fixed height)
        self.preview_holder = ttk.Frame(self.frm_preview, height=220)
        self.preview_holder.pack(fill="x", pady=(6, 6))
        self.preview_holder.pack_propagate(False)
        self.lbl_image_preview = tk.Label(self.preview_holder, bg=controller.PRIMARY_BG)
        self.lbl_image_preview.pack(anchor="center")

        # text area
        frm_text = ttk.Frame(self.frm_content)
        frm_text.pack(fill="both", expand=True, pady=(2, 6))
        self.text_page = tk.Text(frm_text, height=10, font=controller.font_normal,
                                 wrap="word", bg=controller.text_bg, fg=controller.text_fg)
        self.text_page.pack(fill="both", expand=True)

        # bottom buttons (fixed)
        self.frm_buttons = ttk.Frame(self)
        self.frm_buttons.pack(side="bottom", fill="x", pady=(6, 6))

        self.btn_back = tk.Button(self.frm_buttons, text="Zurück", font=controller.font_normal,
                                  bg=controller.button_bg, fg=controller.button_fg, command=self.on_back)
        self.btn_back.pack(side="left", expand=True, fill="x", padx=6)

        self.btn_save = tk.Button(self.frm_buttons, text="Speichern", font=controller.font_normal,
                                  bg=controller.button_bg, fg=controller.button_fg, command=self.on_save)
        self.btn_save.pack(side="left", expand=True, fill="x", padx=6)

    # lifecycle
    def on_show(self):
        if not self.controller.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials bearbeiten.")
            self.controller.show_frame("HomeScreen")
            return

        data = self.controller.get_current_tutorial()
        if not data:
            self.controller.show_frame("HomeScreen")
            return

        self.tutorial_data = data
        self.current_page_index = 0

        self.entry_tutorial_name.delete(0, tk.END)
        self.entry_tutorial_name.insert(0, self.tutorial_data.get("name", ""))

        self.load_page_into_gui()

    def ensure_loaded(self):
        if self.tutorial_data is None:
            self.tutorial_data = self.controller.get_current_tutorial() or {"id": None, "name": "", "pages": []}

    def save_gui_into_current_page(self):
        self.ensure_loaded()
        pages = self.tutorial_data.setdefault("pages", [])
        if not pages:
            pages.append({"title": "", "image": "", "text": ""})
        if not (0 <= self.current_page_index < len(pages)):
            return
        page = pages[self.current_page_index]
        page["title"] = self.entry_page_title.get()
        page["image"] = self.entry_image.get()
        page["text"] = self.text_page.get("1.0", tk.END).rstrip("\n")

    def load_page_into_gui(self):
        self.ensure_loaded()
        pages = self.tutorial_data.setdefault("pages", [])
        if not pages:
            pages.append({"title": "", "image": "", "text": ""})
            self.current_page_index = 0
        if self.current_page_index >= len(pages):
            self.current_page_index = len(pages) - 1

        page = pages[self.current_page_index]

        # ensure title entry exists (create if needed)
        if not hasattr(self, "entry_page_title"):
            frm_page_title = ttk.Frame(self.frm_content)
            frm_page_title.pack(fill="x", pady=(2, 6), before=self.frm_preview)
            ttk.Label(frm_page_title, text="Seitentitel:", font=self.controller.font_normal).pack(side="left")
            self.entry_page_title = tk.Entry(frm_page_title, font=self.controller.font_normal,
                                             bg=self.controller.entry_bg, fg=self.controller.entry_fg)
            self.entry_page_title.pack(side="left", fill="x", expand=True, padx=(6, 0))

        self.entry_page_title.delete(0, tk.END)
        self.entry_page_title.insert(0, page.get("title", ""))

        self.entry_image.delete(0, tk.END)
        self.entry_image.insert(0, page.get("image", ""))

        self.text_page.delete("1.0", tk.END)
        self.text_page.insert("1.0", page.get("text", ""))

        # preview
        img_ref = page.get("image", "")
        if img_ref:
            tid = self.controller.current_tutorial_id
            img_path = img_ref if os.path.isabs(img_ref) else os.path.join(ds.tutorial_images_dir(tid), img_ref)
            max_w = int(self.winfo_width() * 0.8 or 600)
            max_h = int(220 * 0.9)
            img = load_image_for_tk(img_path, max_width=max_w, max_height=max_h)
            if img:
                self.lbl_image_preview.config(image=img)
                self._preview_img_ref = img
            else:
                self.lbl_image_preview.config(image="")
                self._preview_img_ref = None
        else:
            self.lbl_image_preview.config(image="")
            self._preview_img_ref = None

        total = len(pages)
        self.lbl_page_info.config(text=f"Seite {self.current_page_index + 1} / {total}")

        self.btn_prev_page.config(state="normal" if self.current_page_index > 0 else "disabled")
        self.btn_next_page.config(state="normal" if self.current_page_index < total - 1 else "disabled")

    # navigation / pages
    def on_prev_page(self):
        self.save_gui_into_current_page()
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.load_page_into_gui()

    def on_next_page(self):
        self.save_gui_into_current_page()
        pages = self.tutorial_data.setdefault("pages", [])
        if self.current_page_index < len(pages) - 1:
            self.current_page_index += 1
            self.load_page_into_gui()

    def on_add_page(self):
        self.save_gui_into_current_page()
        pages = self.tutorial_data.setdefault("pages", [])
        new_page = {"title": f"Seite {len(pages) + 1}", "image": "", "text": ""}
        insert_index = self.current_page_index + 1
        pages.insert(insert_index, new_page)
        self.current_page_index = insert_index
        self.load_page_into_gui()

    # image selection
    def on_pick_image(self):
        filename = filedialog.askopenfilename(
            title="Bild auswählen",
            filetypes=[("Bilder", "*.png *.gif *.jpg *.jpeg *.bmp"), ("Alle Dateien", "*.*")]
        )
        if not filename:
            return

        tid = self.controller.current_tutorial_id
        if not tid:
            messagebox.showerror("Fehler", "Kein Tutorial ausgewählt.")
            return

        try:
            new_name = ds.copy_image_into_tutorial(tid, filename)
        except Exception as e:
            messagebox.showerror("Fehler beim Kopieren", f"Bild konnte nicht kopiert werden:\n{e}")
            return

        self.entry_image.delete(0, tk.END)
        self.entry_image.insert(0, new_name)

        img_path = os.path.join(ds.tutorial_images_dir(tid), new_name)
        max_w = int(self.winfo_width() * 0.7 or 600)
        max_h = int(220 * 0.9)
        img = load_image_for_tk(img_path, max_width=max_w, max_height=max_h)
        if img:
            self.lbl_image_preview.config(image=img)
            self._preview_img_ref = img
        else:
            self.lbl_image_preview.config(image="")
            self._preview_img_ref = None

        # speichern in cache
        self.save_gui_into_current_page()

    # footer
    def on_back(self):
        self.on_save()
        self.controller.show_frame("HomeScreen")

    def on_save(self):
        self.save_gui_into_current_page()
        if not self.tutorial_data:
            return
        self.tutorial_data["name"] = self.entry_tutorial_name.get() or "Unbenannt"
        self.controller.save_current_tutorial(self.tutorial_data)
        messagebox.showinfo("Gespeichert", "Tutorial wurde gespeichert.")
