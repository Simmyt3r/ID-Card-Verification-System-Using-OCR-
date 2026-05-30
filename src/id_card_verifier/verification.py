"""Verification workflow for OCR text and challenge answers."""

from __future__ import annotations

from .database import StudentRepository
from .models import Student, VerificationResult
from .ocr import extract_matric_number


class VerificationService:
    """Coordinates OCR text matching and security-question verification."""

    def __init__(self, repository: StudentRepository) -> None:
        self.repository = repository

    def verify_card_text(self, card_text: str) -> VerificationResult:
        """Match extracted ID card text to a registered student."""

        matric_number = extract_matric_number(card_text)
        if not matric_number:
            return VerificationResult(
                matched=False,
                message="No valid matriculation number was found in the card text.",
            )

        student = self.repository.find_by_matric(matric_number)
        if not student:
            return VerificationResult(
                matched=False,
                message=f"Matric number {matric_number} is not registered.",
            )

        normalized_text = card_text.casefold()
        name_matches = student.full_name.casefold() in normalized_text
        department_matches = student.department.casefold() in normalized_text

        if not name_matches and not department_matches:
            return VerificationResult(
                matched=False,
                message=(
                    f"Matric number {student.matric_number} exists, but the card text "
                    "does not include the expected name or department."
                ),
                student=student,
            )

        return VerificationResult(
            matched=True,
            message=f"Card matched registered student {student.full_name}.",
            student=student,
        )

    @staticmethod
    def challenge_question(student: Student) -> str:
        """Return the security question asked after a card match."""

        return f"What year were you admitted to {student.department}?"

    @staticmethod
    def verify_secret_answer(student: Student, answer: str) -> bool:
        """Check the answer to the second-factor security question."""

        return answer.strip().casefold() == student.secret_answer.strip().casefold()
