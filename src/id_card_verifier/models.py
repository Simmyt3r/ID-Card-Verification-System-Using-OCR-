"""Domain models used by the ID card verifier."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Student:
    """A registered student record."""

    matric_number: str
    full_name: str
    department: str
    faculty: str
    admission_year: str
    level: str
    secret_answer: str


@dataclass(frozen=True)
class VerificationResult:
    """Result returned after matching OCR text against database records."""

    matched: bool
    message: str
    student: Student | None = None
