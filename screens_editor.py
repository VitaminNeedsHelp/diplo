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

        self.frm_content = ttk.Frame(self)
        self.frm_content.pack(fill="both", expand=True)

        # Tutorial Titel
        frm_name = ttk.Frame(self.frm_content)
        frm_name.pack(fill="x", pady=(2, 6))
        ttk.Label(frm_name, text="Tutorial-Titel:", font=controller.font_normal).pack(side="left")
        self.entry_tutorial_name = tk.Entry(
            frm_name, font=controller.font_normal,
            bg=controller.entry_bg, fg=controller.entry_fg
        )
        self.entry_tutorial_name.pack(side="left", fill="x", expand=True, padx=(6, 0))

        # Seiten Navigation
        frm_page_nav = ttk.Frame(self.frm_content)
        frm_page_nav.pack(fill="x", pady=(4, 6))

        self.btn_prev_page = tk.Button(
            frm_page_nav, text="◀ Seite",
            bg=controller.button_bg, fg=controller.button_fg,
            command=self.on_prev_page
        )
        self.btn_prev_page.pack(side="left")

        self.lbl_page_info = ttk.Label(frm_page_nav, font=controller.font_normal)
        self.lbl_page_info.pack(side="left", expand=True)

        self.btn_next_page = tk.Button(
            frm_page_nav, text="Seite ▶",
            bg=controller.button_bg, fg=controller.button_fg,
            command=self.on_next_page
        )
        self.btn_next_page.pack(side="left")

        # 🆕 Seite löschen
        self.btn_delete_page = tk.Button(
            frm_page_nav,
            text="🗑 Seite löschen",
            font=controller.font_small,
            bg="#b03030",
            fg="#ffffff",
            activebackground="#b03030",
            activeforeground="#ffffff",
            command=self.on_delete_page
        )
        self.btn_delete_page.pack(side="right", padx=5)

        # Buttons hinzufügen
        self.btn_add_content = tk.Button(
            self.frm_content, text="Inhalts-Seite hinzufügen",
            bg=controller.button_bg, fg=controller.button_fg,
            command=self.on_add_content_page
        )
        self.btn_add_content.pack(fill="x", pady=(4, 2))

        self.btn_add_quiz = tk.Button(
            self.frm_content, text="Quiz-Seite hinzufügen",
            bg=controller.button_bg, fg=controller.button_fg,
            command=self.on_add_quiz_page
        )
        self.btn_add_quiz.pack(fill="x", pady=(0, 8))

        # ---------- CONTENT EDITOR ----------
        self.frm_content_editor = ttk.Frame(self.frm_content)

        ttk.Label(self.frm_content_editor, text="Seitentitel:").pack(anchor="w")
        self.entry_page_title = tk.Entry(
            self.frm_content_editor,
            bg=controller.entry_bg, fg=controller.entry_fg
        )
        self.entry_page_title.pack(fill="x", pady=(0, 4))

        ttk.Label(self.frm_content_editor, text="Bild:").pack(anchor="w")
        frm_img = ttk.Frame(self.frm_content_editor)
        frm_img.pack(fill="x", pady=(0, 4))
        self.entry_image = tk.Entry(
            frm_img, bg=controller.entry_bg, fg=controller.entry_fg
        )
        self.entry_image.pack(side="left", fill="x", expand=True)
        tk.Button(frm_img, text="Auswählen…", command=self.on_pick_image)\
            .pack(side="left", padx=4)

        self.preview_holder = ttk.Frame(self.frm_content_editor, height=220)
        self.preview_holder.pack(fill="x", pady=6)
        self.preview_holder.pack_propagate(False)
        self.lbl_image_preview = tk.Label(self.preview_holder, bg=controller.PRIMARY_BG)
        self.lbl_image_preview.pack(anchor="center")

        ttk.Label(self.frm_content_editor, text="Text:").pack(anchor="w")
        self.text_page = tk.Text(
            self.frm_content_editor, height=8,
            bg=controller.text_bg, fg=controller.text_fg, wrap="word"
        )
        self.text_page.pack(fill="both", expand=True)

        # ---------- QUIZ EDITOR ----------
        self.frm_quiz_editor = ttk.Frame(self.frm_content)

        ttk.Label(self.frm_quiz_editor, text="Frage:").pack(anchor="w")
        self.entry_question = tk.Entry(
            self.frm_quiz_editor,
            bg=controller.entry_bg, fg=controller.entry_fg
        )
        self.entry_question.pack(fill="x", pady=(0, 4))

        ttk.Label(self.frm_quiz_editor, text="Quiz-Bild:").pack(anchor="w")
        frm_qimg = ttk.Frame(self.frm_quiz_editor)
        frm_qimg.pack(fill="x", pady=(0, 4))
        self.entry_quiz_image = tk.Entry(
            frm_qimg, bg=controller.entry_bg, fg=controller.entry_fg
        )
        self.entry_quiz_image.pack(side="left", fill="x", expand=True)
        tk.Button(frm_qimg, text="Auswählen…", command=self.on_pick_quiz_image)\
            .pack(side="left", padx=4)

        ttk.Label(self.frm_quiz_editor, text="Antworten (eine pro Zeile):").pack(anchor="w")
        self.text_options = tk.Text(
            self.frm_quiz_editor, height=5,
            bg=controller.text_bg, fg=controller.text_fg
        )
        self.text_options.pack(fill="x", pady=(0, 4))

        ttk.Label(self.frm_quiz_editor, text="Index der richtigen Antwort (0-basiert):").pack(anchor="w")
        self.entry_correct = tk.Entry(
            self.frm_quiz_editor, width=5,
            bg=controller.entry_bg, fg=controller.entry_fg
        )
        self.entry_correct.pack(anchor="w", pady=(0, 4))

        ttk.Label(self.frm_quiz_editor, text="Erklärung:").pack(anchor="w")
        self.text_explanation = tk.Text(
            self.frm_quiz_editor, height=3,
            bg=controller.text_bg, fg=controller.text_fg
        )
        self.text_explanation.pack(fill="x")

        # Footer
        frm_footer = ttk.Frame(self)
        frm_footer.pack(fill="x", pady=6)
        tk.Button(frm_footer, text="Zurück", command=self.on_back)\
            .pack(side="left", expand=True, fill="x", padx=4)
        tk.Button(frm_footer, text="Speichern", command=self.on_save)\
            .pack(side="left", expand=True, fill="x", padx=4)

    # ---------------- Lifecycle ----------------
    def on_show(self):
        if not self.controller.is_admin:
            messagebox.showinfo("Nicht erlaubt", "Nur Administratoren dürfen Tutorials bearbeiten.")
            self.controller.show_frame("HomeScreen")
            return

        self.tutorial_data = self.controller.get_current_tutorial()
        self.current_page_index = 0

        self.entry_tutorial_name.delete(0, tk.END)
        self.entry_tutorial_name.insert(0, self.tutorial_data.get("name", ""))

        self.load_page()

    # ---------------- Page Handling ----------------
    def load_page(self):
        pages = self.tutorial_data["pages"]
        page = pages[self.current_page_index]

        self.lbl_page_info.config(
            text=f"Seite {self.current_page_index + 1} / {len(pages)}"
        )

        self.frm_content_editor.pack_forget()
        self.frm_quiz_editor.pack_forget()

        if page.get("type") == "quiz":
            self.frm_quiz_editor.pack(fill="both", expand=True)
            self.entry_question.delete(0, tk.END)
            self.entry_question.insert(0, page.get("question", ""))
            self.entry_quiz_image.delete(0, tk.END)
            self.entry_quiz_image.insert(0, page.get("image", ""))
            self.text_options.delete("1.0", tk.END)
            self.text_options.insert("1.0", "\n".join(page.get("options", [])))
            self.entry_correct.delete(0, tk.END)
            self.entry_correct.insert(0, str(page.get("correct_index", 0)))
            self.text_explanation.delete("1.0", tk.END)
            self.text_explanation.insert("1.0", page.get("explanation", ""))
            return

        self.frm_content_editor.pack(fill="both", expand=True)
        self.entry_page_title.delete(0, tk.END)
        self.entry_page_title.insert(0, page.get("title", ""))
        self.entry_image.delete(0, tk.END)
        self.entry_image.insert(0, page.get("image", ""))
        self.text_page.delete("1.0", tk.END)
        self.text_page.insert("1.0", page.get("text", ""))

    def save_current_page(self):
        page = self.tutorial_data["pages"][self.current_page_index]

        if page.get("type") == "quiz":
            page["question"] = self.entry_question.get()
            page["image"] = self.entry_quiz_image.get()
            page["options"] = [
                l.strip() for l in self.text_options.get("1.0", tk.END).splitlines()
                if l.strip()
            ]
            page["correct_index"] = int(self.entry_correct.get() or 0)
            page["explanation"] = self.text_explanation.get("1.0", tk.END).strip()
            return

        page["type"] = "content"
        page["title"] = self.entry_page_title.get()
        page["image"] = self.entry_image.get()
        page["text"] = self.text_page.get("1.0", tk.END).strip()

    # ---------------- Navigation ----------------
    def on_prev_page(self):
        self.save_current_page()
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.load_page()

    def on_next_page(self):
        self.save_current_page()
        if self.current_page_index < len(self.tutorial_data["pages"]) - 1:
            self.current_page_index += 1
            self.load_page()

    def on_add_content_page(self):
        self.save_current_page()
        self.tutorial_data["pages"].insert(
            self.current_page_index + 1,
            {"type": "content", "title": "", "image": "", "text": ""}
        )
        self.current_page_index += 1
        self.load_page()

    def on_add_quiz_page(self):
        self.save_current_page()
        self.tutorial_data["pages"].insert(
            self.current_page_index + 1,
            {
                "type": "quiz",
                "question": "",
                "image": "",
                "options": ["Antwort A", "Antwort B"],
                "correct_index": 0,
                "explanation": ""
            }
        )
        self.current_page_index += 1
        self.load_page()

    def on_delete_page(self):
        pages = self.tutorial_data["pages"]
        if len(pages) <= 1:
            messagebox.showinfo("Nicht möglich", "Ein Tutorial muss mindestens eine Seite haben.")
            return

        if not messagebox.askyesno("Seite löschen", "Diese Seite wirklich löschen?"):
            return

        pages.pop(self.current_page_index)
        if self.current_page_index >= len(pages):
            self.current_page_index = len(pages) - 1

        self.load_page()

    # ---------------- Image Picker ----------------
    def on_pick_image(self):
        p = filedialog.askopenfilename()
        if not p:
            return
        name = ds.copy_image_into_tutorial(self.controller.current_tutorial_id, p)
        self.entry_image.delete(0, tk.END)
        self.entry_image.insert(0, name)

    def on_pick_quiz_image(self):
        p = filedialog.askopenfilename()
        if not p:
            return
        name = ds.copy_image_into_tutorial(self.controller.current_tutorial_id, p)
        self.entry_quiz_image.delete(0, tk.END)
        self.entry_quiz_image.insert(0, name)

    # ---------------- Footer ----------------
    def on_save(self):
        self.save_current_page()
        self.tutorial_data["name"] = self.entry_tutorial_name.get()
        self.controller.save_current_tutorial(self.tutorial_data)
        messagebox.showinfo("Gespeichert", "Tutorial gespeichert.")

    def on_back(self):
        self.on_save()
        self.controller.show_frame("HomeScreen")
