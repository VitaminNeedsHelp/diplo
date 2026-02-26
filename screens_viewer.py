import tkinter as tk
from tkinter import ttk
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from image_utils import load_image_for_tk
import data_store as ds
import os
import random


class TutorialViewerScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding=10)

        self.current_page_index = 0
        self.current_img = None
        self.answered_correctly = False

        BG = controller.PRIMARY_BG
        FG = controller.PRIMARY_FG

        # -------- Content --------
        self.frm_content = ttk.Frame(self)
        self.frm_content.pack(fill="both", expand=True)

        self.lbl_tutorial_name = tk.Label(
            self.frm_content,
            font=controller.font_title,
            bg=BG, fg=FG
        )
        self.lbl_tutorial_name.pack(anchor="n", pady=(5, 10))

        self.lbl_page_title = tk.Label(
            self.frm_content,
            font=controller.font_normal,
            bg=BG, fg=FG
        )
        self.lbl_page_title.pack(anchor="n", pady=(5, 5))

        self.lbl_image = tk.Label(self.frm_content, bg=BG)
        self.lbl_image.pack(anchor="n", pady=(5, 5))

        self.lbl_text = tk.Label(
            self.frm_content,
            font=controller.font_normal,
            wraplength=WINDOW_WIDTH - 40,
            justify="left",
            bg=BG, fg=FG
        )
        self.lbl_text.pack(fill="both", expand=True, pady=(5, 10))

        self.quiz_frame = ttk.Frame(self.frm_content)

        # -------- Navigation --------
        self.frm_nav = ttk.Frame(self)
        self.frm_nav.pack(fill="x", padx=10, pady=(5, 5))

        self.btn_prev = tk.Button(
            self.frm_nav,
            text="⬅ Zurück",
            font=controller.font_normal,
            bg=controller.button_bg,
            fg=controller.button_fg,
            activebackground=controller.button_bg,
            activeforeground=controller.button_fg,
            command=self.on_prev
        )
        self.btn_prev.pack(side="left", expand=True, fill="x", padx=5)

        self.lbl_page_info = ttk.Label(self.frm_nav, font=controller.font_normal)
        self.lbl_page_info.pack(side="left", padx=5)

        self.btn_next = tk.Button(
            self.frm_nav,
            text="Weiter ➡",
            font=controller.font_normal,
            bg=controller.button_bg,
            fg=controller.button_fg,
            activebackground=controller.button_bg,
            activeforeground=controller.button_fg,
            command=self.on_next
        )
        self.btn_next.pack(side="left", expand=True, fill="x", padx=5)

        # -------- Home Button --------
        self.btn_home = tk.Button(
            self,
            text="Zurück zum Home-Bildschirm",
            font=controller.font_normal,
            bg=controller.button_bg,
            fg=controller.button_fg,
            activebackground=controller.button_bg,
            activeforeground=controller.button_fg,
            command=lambda: controller.show_frame("HomeScreen")
        )
        self.btn_home.pack(side="bottom", fill="x", padx=15, pady=(0, 10))

    # -------- Lifecycle --------
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
        pages = tutorial.get("pages", [])

        page = pages[self.current_page_index]
        self.lbl_page_info.config(text=f"{self.current_page_index + 1} / {len(pages)}")

        self.quiz_frame.pack_forget()
        for w in self.quiz_frame.winfo_children():
            w.destroy()

        self.lbl_image.config(image="")
        self.current_img = None

        self.btn_prev.config(state="normal" if self.current_page_index > 0 else "disabled")

        if page.get("type") == "quiz":
            self.show_quiz(page)
            return

        self.btn_next.config(state="normal")
        self.lbl_page_title.config(text=page.get("title", ""))
        self.lbl_text.config(text=page.get("text", ""))

        if page.get("image"):
            path = os.path.join(
                ds.tutorial_images_dir(self.controller.current_tutorial_id),
                page["image"]
            )
            img = load_image_for_tk(path, int(WINDOW_WIDTH * 0.9), int(WINDOW_HEIGHT * 0.45))
            if img:
                self.lbl_image.config(image=img)
                self.current_img = img

    def show_quiz(self, page):
        self.answered_correctly = False
        self.btn_next.config(state="disabled")

        self.lbl_page_title.config(text=page.get("question", ""))
        self.lbl_text.config(text="")

        if page.get("image"):
            path = os.path.join(
                ds.tutorial_images_dir(self.controller.current_tutorial_id),
                page["image"]
            )
            img = load_image_for_tk(path, int(WINDOW_WIDTH * 0.8), int(WINDOW_HEIGHT * 0.3))
            if img:
                self.lbl_image.config(image=img)
                self.current_img = img

        self.quiz_frame.pack(pady=10)

        options = list(enumerate(page.get("options", [])))
        random.shuffle(options)

        grid = ttk.Frame(self.quiz_frame)
        grid.pack()

        for i, (idx, txt) in enumerate(options):
            btn = tk.Button(
                grid,
                text=txt,
                width=20,
                height=3,
                font=self.controller.font_normal,
                bg=self.controller.button_bg,
                fg=self.controller.button_fg,
                activebackground=self.controller.button_bg,
                activeforeground=self.controller.button_fg,
                wraplength=180,
                justify="center",
                command=lambda x=idx: self.answer(x, page)
            )
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)

    def answer(self, selected, page):
        if self.answered_correctly:
            return

        if selected == page.get("correct_index"):
            self.lbl_text.config(text="✅ Richtig\n\n" + page.get("explanation", ""))
            self.answered_correctly = True
            self.btn_next.config(state="normal")
        else:
            self.lbl_text.config(text="❌ Falsch\n\n" + page.get("explanation", ""))

    def on_prev(self):
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.load_page()

    def on_next(self):
        tutorial = self.controller.get_current_tutorial()
        page = tutorial["pages"][self.current_page_index]

        if page.get("type") == "quiz" and not self.answered_correctly:
            return

        if self.current_page_index < len(tutorial["pages"]) - 1:
            self.current_page_index += 1
            self.load_page()
