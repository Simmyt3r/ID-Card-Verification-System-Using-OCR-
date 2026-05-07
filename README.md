# 🪪 Automated Student ID Card Verification System

> *Like a super-smart security guard that never gets tired, never gets tricked, and always asks the right questions.*

---

## 🧒 What does this project do? (Explain Like I'm 5)

Imagine your school has a security guard at the gate. Every time a student walks in, the guard looks at their ID card and says *"okay, you can enter."*

But what if someone **stole** another student's ID card and tried to use it? The guard might not notice. That's a problem.

This project builds a **computer program** that acts like a much smarter guard. Here's what it does, step by step:

### Step 1 — It reads your ID card 👀
You hold your card up to a **webcam**. The computer takes a photo and reads all the text on the card — your name, your matric number, your department — just like how you scan a barcode at a supermarket, but for words.

### Step 2 — It checks if you're real 🗂️
The computer then goes into a **database** (think of it like a big register book, but digital) and checks: *"Does this person actually go to this school?"* If the card is fake or the details don't match — **access denied**.

### Step 3 — It asks you a secret question 🗣️
Even if the card is real, the computer still isn't 100% sure *you're* the owner. So it **speaks out loud** (using text-to-speech) and asks you a question that only the real student would know — like your year of admission or your faculty. You type your answer. Get it right — **you're in**. Get it wrong — **nope**.

---

## 🛠️ What tools is it built with?

| Tool | What it does in simple terms |
|------|------------------------------|
| **Python** | The main programming language — like the brain of the project |
| **OpenCV** | Handles the webcam and cleans up the photo before reading it |
| **Tesseract OCR** | Reads the text off the ID card image |
| **SQLite/MySQL** | Stores all the student records |
| **pyttsx3** | Makes the computer speak the security question out loud |

---

## 🔐 Why three steps instead of one?

Think of it like a bank vault:
- One lock is okay.
- **Three locks** is much harder to break.

A thief might steal your ID card (Step 1 fooled), but they probably **don't know your academic details** (Step 3 stops them cold). That's the whole idea — layers of security.

---

## 🏫 Where is it meant to be used?

**Nigerian Army University Biu (NAUB)** — specifically to fix the problem of students or outsiders using fake or stolen ID cards to access restricted areas on campus.

---

## ⚠️ Known Limitations (honest talk)

- If the lighting is bad, the camera might misread the card.
- If someone knows all your school details really well, they could still try to fool Step 3.
- The system works offline and is desktop-only for now — no mobile app yet.

---

## 👩‍💻 Who built this?

**Moses Thelma Marvellous**
Department of Cyber Security, Faculty of Computing
Nigerian Army University, Biu
Matric No: CYB/23U/4190

---

## 📄 Academic Context

This is a final year undergraduate project submitted in partial fulfilment of the requirements for the award of a B.Sc. in Cyber Security at NAUB.

---

*"A stolen card gets you to the door. It doesn't get you through it."*
