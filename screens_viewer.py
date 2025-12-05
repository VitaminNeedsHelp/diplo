import tkinter as tk
from tkinter import ttk
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from image_utils import load_image_for_tk
import data_store as ds
import os


class TutorialViewerScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding=10)

        self.current_page_index = 0
        self.current_img = None

        BG = getattr(controller, "PRIMARY_BG", "#637DFF")
        FG = getattr(controller, "PRIMARY_FG", "#FFFFFF")

        # content frame expand
        self.frm_content = ttk.Frame(self)
        self.frm_content.pack(fill="both", expand=True)

        # nav fixed bottom
        self.frm_nav = ttk.Frame(self)
        self.frm_nav.pack(side="bottom", fill="x", padx=10, pady=10)

        # Title
        self.lbl_tutorial_name = tk.Label(self.frm_content, text="Tutorial", font=controller.font_title,
                                          bg=BG, fg=FG)
        self.lbl_tutorial_name.pack(anchor="n", pady=(5, 10))

        self.lbl_page_title = tk.Label(self.frm_content, text="", font=controller.font_normal, bg=BG, fg=FG)
        self.lbl_page_title.pack(anchor="n", pady=(5, 5))

        # image
        self.lbl_image = tk.Label(self.frm_content, bg=BG)
        self.lbl_image.pack(anchor="n", pady=(5, 5))

        # text area expand
        self.frm_text = ttk.Frame(self.frm_content)
        self.frm_text.pack(fill="both", expand=True, pady=(5, 10))
        self.lbl_text = tk.Label(self.frm_text, text="", font=controller.font_normal,
                                 wraplength=WINDOW_WIDTH - 40, justify="left",
                                 bg=BG, fg=FG, anchor="n")
        self.lbl_text.pack(fill="both", expand=True)

        # nav buttons
        self.btn_prev = tk.Button(self.frm_nav, text="⬅ Zurück", font=controller.font_normal,
                                  bg=controller.button_bg, fg=controller.button_fg, command=self.on_prev)
        self.btn_prev.pack(side="left", expand=True, fill="x", padx=5)

        self.lbl_page_info = ttk.Label(self.frm_nav, text="1/1", font=controller.font_normal)
        self.lbl_page_info.pack(side="left", padx=5)

        self.btn_next = tk.Button(self.frm_nav, text="Weiter ➡", font=controller.font_normal,
                                  bg=controller.button_bg, fg=controller.button_fg, command=self.on_next)
        self.btn_next.pack(side="left", expand=True, fill="x", padx=5)

        # home button fixed under nav
        self.btn_home = tk.Button(self, text="Zurück zum Home-Bildschirm", font=controller.font_normal,
                                  bg=controller.button_bg, fg=controller.button_fg,
                                  command=lambda: controller.show_frame("HomeScreen"))
        self.btn_home.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

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
            self.lbl_page_title.config(text="(keine Seiten)")
            self.lbl_text.config(text="Dieses Tutorial enthält keine Seiten.")
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

        self.lbl_page_title.config(text=page.get("title") or "(kein Seitentitel)")
        self.lbl_text.config(text=page.get("text") or "(kein Text)")

        img_path = page.get("image", "") or ""
        if img_path:
            tid = self.controller.current_tutorial_id
            load_path = img_path if os.path.isabs(img_path) else os.path.join(ds.tutorial_images_dir(tid), img_path)
            max_w = int(WINDOW_WIDTH * 0.9)
            max_h = int(WINDOW_HEIGHT * 0.45)
            img = load_image_for_tk(load_path, max_width=max_w, max_height=max_h)
            if img is not None:
                self.lbl_image.config(image=img)
                self.current_img = img
            else:
                self.lbl_image.config(image="")
                self.current_img = None
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
