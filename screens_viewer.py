import tkinter as tk
from tkinter import ttk
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from image_utils import load_image_for_tk


class TutorialViewerScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding=10)

        self.current_page_index = 0
        self.current_img = None

        self.lbl_tutorial_name = ttk.Label(self, text="Tutorial", font=controller.font_title)
        self.lbl_tutorial_name.pack(anchor="n", pady=(5, 10))

        self.lbl_page_title = ttk.Label(self, text="", font=controller.font_normal)
        self.lbl_page_title.pack(anchor="n", pady=(5, 5))

        self.lbl_image = ttk.Label(self)
        self.lbl_image.pack(anchor="n", pady=(5, 5))

        self.lbl_text = ttk.Label(
            self, text="", font=controller.font_normal,
            wraplength=WINDOW_WIDTH - 40, justify="left"
        )
        self.lbl_text.pack(anchor="n", pady=(5, 10))

        frm_nav = ttk.Frame(self)
        frm_nav.pack(fill="x", pady=(10, 10))

        self.btn_prev = tk.Button(
            frm_nav, text="⬅ Zurück",
            font=controller.font_normal,
            command=self.on_prev
        )
        self.btn_prev.pack(side="left", expand=True, fill="x", padx=5)

        self.lbl_page_info = ttk.Label(frm_nav, text="1/1", font=controller.font_normal)
        self.lbl_page_info.pack(side="left")

        self.btn_next = tk.Button(
            frm_nav, text="Weiter ➡",
            font=controller.font_normal,
            command=self.on_next
        )
        self.btn_next.pack(side="left", expand=True, fill="x", padx=5)

        btn_home = tk.Button(
            self, text="Zurück zum Home-Bildschirm",
            font=controller.font_normal,
            command=lambda: controller.show_frame("HomeScreen")
        )
        btn_home.pack(fill="x")

    def on_show(self):
        tutorial = self.controller.get_current_tutorial()
        if not tutorial:
            self.controller.show_frame("HomeScreen")
            return
        self.current_page_index = 0
        self.lbl_tutorial_name.config(text=tutorial.get("name", "Tutorial"))
        self.load_page()

    def load_page(self):
        tutorial = self.controller.get_current_tutorial()
        if not tutorial:
            return
        pages = tutorial.get("pages") or []
        if not pages:
            self.lbl_page_title.config(text="Keine Seiten")
            self.lbl_text.config(text="")
            self.lbl_image.config(image="")
            self.current_img = None
            self.lbl_page_info.config(text="0/0")
            self.btn_prev.config(state="disabled")
            self.btn_next.config(state="disabled")
            return

        if self.current_page_index < 0:
            self.current_page_index = 0
        if self.current_page_index >= len(pages):
            self.current_page_index = len(pages) - 1

        page = pages[self.current_page_index]
        self.lbl_page_title.config(text=page.get("title", ""))

        self.lbl_text.config(text=page.get("text", ""))

        img_path = page.get("image", "")
        img = load_image_for_tk(
            img_path,
            max_width=int(WINDOW_WIDTH * 0.9),
            max_height=int(WINDOW_HEIGHT * 0.4)
        )
        if img is not None:
            self.lbl_image.config(image=img)
            self.current_img = img
        else:
            self.lbl_image.config(image="")
            self.current_img = None

        total = len(pages)
        self.lbl_page_info.config(text=f"{self.current_page_index + 1} / {total}")

        self.btn_prev.config(state="normal" if self.current_page_index > 0 else "disabled")
        self.btn_next.config(state="normal" if self.current_page_index < total - 1 else "disabled")

    def on_prev(self):
        self.current_page_index -= 1
        self.load_page()

    def on_next(self):
        self.current_page_index += 1
        self.load_page()
