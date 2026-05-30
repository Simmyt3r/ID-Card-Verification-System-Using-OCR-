"""Tkinter desktop application for the ID card verification workflow."""

from __future__ import annotations

from pathlib import Path
from tkinter import END, LEFT, RIGHT, BOTH, X, filedialog, messagebox, scrolledtext, ttk
import tkinter as tk

from .database import StudentRepository
from .ocr import capture_image_from_webcam, read_text_from_image
from .speech import speak
from .verification import VerificationService

CAPTURE_PATH = Path(__file__).resolve().parents[2] / "data" / "latest_capture.jpg"


class IDCardVerifierApp(tk.Tk):
    """Desktop GUI designed to run directly from PyCharm."""

    def __init__(self) -> None:
        super().__init__()
        self.title("ID Card Verification System")
        self.geometry("920x680")
        self.minsize(820, 600)

        self.repository = StudentRepository()
        self.service = VerificationService(self.repository)
        self.current_student = None

        self._build_interface()
        self._load_sample_hint()
        self._refresh_students()

    def _build_interface(self) -> None:
        main = ttk.Frame(self, padding=16)
        main.pack(fill=BOTH, expand=True)

        heading = ttk.Label(
            main,
            text="Automated Student ID Card Verification System",
            font=("Arial", 18, "bold"),
        )
        heading.pack(anchor="w")

        subheading = ttk.Label(
            main,
            text="Load a card image, capture from webcam, or paste OCR text manually.",
        )
        subheading.pack(anchor="w", pady=(0, 12))

        button_row = ttk.Frame(main)
        button_row.pack(fill=X, pady=(0, 8))

        ttk.Button(button_row, text="Load ID Card Image", command=self.load_image).pack(side=LEFT, padx=(0, 8))
        ttk.Button(button_row, text="Capture From Webcam", command=self.capture_webcam).pack(side=LEFT, padx=(0, 8))
        ttk.Button(button_row, text="Verify Card Text", command=self.verify_card_text).pack(side=LEFT, padx=(0, 8))
        ttk.Button(button_row, text="Clear", command=self.clear_form).pack(side=LEFT)

        panes = ttk.PanedWindow(main, orient=tk.HORIZONTAL)
        panes.pack(fill=BOTH, expand=True)

        left_panel = ttk.Frame(panes, padding=(0, 0, 8, 0))
        right_panel = ttk.Frame(panes, padding=(8, 0, 0, 0))
        panes.add(left_panel, weight=3)
        panes.add(right_panel, weight=2)

        ttk.Label(left_panel, text="Extracted or pasted ID card text", font=("Arial", 11, "bold")).pack(anchor="w")
        self.card_text = scrolledtext.ScrolledText(left_panel, wrap=tk.WORD, height=16)
        self.card_text.pack(fill=BOTH, expand=True, pady=(4, 12))

        challenge = ttk.LabelFrame(left_panel, text="Second-factor security question", padding=12)
        challenge.pack(fill=X)

        self.question_var = tk.StringVar(value="Verify a card first to show the security question.")
        ttk.Label(challenge, textvariable=self.question_var, wraplength=520).pack(anchor="w")

        answer_row = ttk.Frame(challenge)
        answer_row.pack(fill=X, pady=(8, 0))
        self.answer_var = tk.StringVar()
        ttk.Entry(answer_row, textvariable=self.answer_var).pack(side=LEFT, fill=X, expand=True, padx=(0, 8))
        ttk.Button(answer_row, text="Submit Answer", command=self.submit_answer).pack(side=RIGHT)

        status_box = ttk.LabelFrame(right_panel, text="Verification status", padding=12)
        status_box.pack(fill=X)
        self.status_var = tk.StringVar(value="Waiting for ID card text.")
        self.status_label = ttk.Label(status_box, textvariable=self.status_var, wraplength=320, foreground="#1f2937")
        self.status_label.pack(anchor="w")

        student_box = ttk.LabelFrame(right_panel, text="Registered demo students", padding=12)
        student_box.pack(fill=BOTH, expand=True, pady=(12, 0))
        columns = ("matric", "name", "department")
        self.student_table = ttk.Treeview(student_box, columns=columns, show="headings", height=10)
        self.student_table.heading("matric", text="Matric No")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("department", text="Department")
        self.student_table.column("matric", width=105)
        self.student_table.column("name", width=155)
        self.student_table.column("department", width=130)
        self.student_table.pack(fill=BOTH, expand=True)

    def _load_sample_hint(self) -> None:
        sample = (
            "NIGERIAN ARMY UNIVERSITY BIU\n"
            "Name: Moses Thelma Marvellous\n"
            "Matric No: CYB/23U/4190\n"
            "Department: Cyber Security\n"
            "Faculty: Computing\n"
        )
        self.card_text.insert("1.0", sample)

    def _refresh_students(self) -> None:
        self.student_table.delete(*self.student_table.get_children())
        for student in self.repository.all_students():
            self.student_table.insert("", END, values=(student.matric_number, student.full_name, student.department))

    def load_image(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Select ID card image",
            filetypes=(
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"),
                ("All files", "*.*"),
            ),
        )
        if not file_path:
            return
        self._ocr_image(Path(file_path))

    def capture_webcam(self) -> None:
        try:
            image_path = capture_image_from_webcam(CAPTURE_PATH)
        except Exception as exc:
            messagebox.showerror("Webcam error", str(exc))
            return
        self._ocr_image(image_path)

    def _ocr_image(self, image_path: Path) -> None:
        try:
            text = read_text_from_image(image_path)
        except Exception as exc:
            messagebox.showerror("OCR error", str(exc))
            return
        self.card_text.delete("1.0", END)
        self.card_text.insert("1.0", text)
        self.status_var.set(f"OCR completed for {image_path.name}. Click Verify Card Text.")

    def verify_card_text(self) -> None:
        result = self.service.verify_card_text(self.card_text.get("1.0", END))
        self.current_student = result.student if result.matched else None
        self.answer_var.set("")
        self.status_var.set(result.message)

        if result.matched and result.student:
            question = self.service.challenge_question(result.student)
            self.question_var.set(question)
            spoke = speak(question)
            if not spoke:
                self.status_var.set(result.message + " Text-to-speech is unavailable, so read the question on screen.")
        else:
            self.question_var.set("Card verification failed. Fix the text or use another card.")

    def submit_answer(self) -> None:
        if not self.current_student:
            messagebox.showwarning("No verified card", "Verify a registered ID card before answering the question.")
            return

        if self.service.verify_secret_answer(self.current_student, self.answer_var.get()):
            self.status_var.set(f"ACCESS GRANTED: Welcome, {self.current_student.full_name}.")
            messagebox.showinfo("Access granted", "Student identity verified successfully.")
        else:
            self.status_var.set("ACCESS DENIED: The security answer is incorrect.")
            messagebox.showerror("Access denied", "The answer does not match the registered student record.")

    def clear_form(self) -> None:
        self.card_text.delete("1.0", END)
        self.answer_var.set("")
        self.current_student = None
        self.question_var.set("Verify a card first to show the security question.")
        self.status_var.set("Waiting for ID card text.")


def main() -> None:
    """Launch the desktop application."""

    app = IDCardVerifierApp()
    app.mainloop()


if __name__ == "__main__":
    main()
