# 🪪 Automated Student ID Card Verification System

A PyCharm-friendly Python desktop application that verifies student ID cards with OCR, checks the extracted details against a SQLite student database, and then asks a second-factor security question before granting access.

> A stolen card gets you to the door. It does not get you through it.

---

## ✅ What the application does

1. **Reads an ID card** from either:
   - an uploaded image,
   - a webcam capture, or
   - manually pasted OCR text for testing.
2. **Extracts the matriculation number** from the card text.
3. **Checks the student database** to confirm that the matric number belongs to a registered student.
4. **Verifies card consistency** by checking that the extracted text includes the expected student name or department.
5. **Asks a secret question** using on-screen text and optional text-to-speech.
6. **Grants or denies access** based on the answer.

The app ships with demo students, so it runs immediately after setup.

---

## 🧰 Technology stack

| Tool | Purpose |
| --- | --- |
| Python 3.10+ | Main programming language |
| Tkinter | Desktop user interface that runs well from PyCharm |
| SQLite | Local student database |
| OpenCV | Webcam capture and image preprocessing |
| Tesseract + pytesseract | OCR text extraction from ID card images |
| pyttsx3 | Offline text-to-speech for the security question |

---

## 📁 Project structure

```text
.
├── main.py                         # Run this file in PyCharm
├── pyproject.toml                  # Package metadata and dependencies
├── requirements.txt                # pip dependencies
├── src/id_card_verifier/
│   ├── app.py                      # Tkinter GUI
│   ├── database.py                 # SQLite repository and demo seed data
│   ├── models.py                   # Student and verification dataclasses
│   ├── ocr.py                      # OCR, webcam, and matric extraction helpers
│   ├── speech.py                   # Optional text-to-speech helper
│   └── verification.py             # Verification business logic
└── tests/test_verification.py      # Unit tests for the core workflow
```

---

## 🚀 Run in PyCharm

1. Open this repository folder in **PyCharm**.
2. Create a virtual environment when PyCharm prompts you, or go to:
   - `File` → `Settings` → `Project` → `Python Interpreter` → `Add Interpreter`.
3. Install dependencies in PyCharm's terminal:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Install the Tesseract desktop application:
   - **Windows:** install from the UB Mannheim Tesseract builds, then ensure `tesseract.exe` is on your `PATH`.
   - **macOS:** `brew install tesseract`
   - **Ubuntu/Debian:** `sudo apt install tesseract-ocr`

5. Right-click `main.py` and choose **Run 'main'**.

> If OpenCV, Tesseract, or pyttsx3 are not installed yet, the app still opens. You can paste text manually and test the verification workflow without camera/OCR/audio.

---

## 🧪 Quick demo without camera or OCR

When the app opens, it preloads this sample ID text:

```text
NIGERIAN ARMY UNIVERSITY BIU
Name: Moses Thelma Marvellous
Matric No: CYB/23U/4190
Department: Cyber Security
Faculty: Computing
```

Click **Verify Card Text**, then answer the displayed security question with:

```text
2023
```

The application should show **ACCESS GRANTED**.

---

## 🗃️ Demo database records

The SQLite database is created automatically at `data/students.db` the first time the app runs. Demo records are inserted with `INSERT OR IGNORE`, so your local changes will not be overwritten on every launch.

| Matric number | Name | Department | Secret answer |
| --- | --- | --- | --- |
| CYB/23U/4190 | Moses Thelma Marvellous | Cyber Security | 2023 |
| CSC/22U/1001 | Aisha Ibrahim | Computer Science | 2022 |
| IFT/24U/2048 | Daniel Okoro | Information Technology | 2024 |

To add real students, open `src/id_card_verifier/database.py` and update `SAMPLE_STUDENTS`, or edit `data/students.db` with any SQLite browser.

---

## 🧪 Run tests

```bash
python -m pytest
```

If `pytest` is not installed:

```bash
python -m pip install pytest
```

---

## ⚠️ Known limitations

- OCR accuracy depends on lighting, camera quality, card design, and Tesseract installation.
- The current app is a local desktop prototype and is not a networked access-control system.
- The sample second-factor question uses admission year. A production system should support stronger institution-managed challenge questions.
- SQLite is suitable for a local prototype. A deployed campus system should use a centrally managed database with authentication, auditing, backups, and role-based access controls.

---

## 👩‍💻 Academic context

Built for a final-year undergraduate project about an automated student ID card verification system for Nigerian Army University Biu (NAUB), Department of Cyber Security, Faculty of Computing.
