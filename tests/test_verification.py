from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from id_card_verifier.database import StudentRepository
from id_card_verifier.ocr import extract_matric_number
from id_card_verifier.verification import VerificationService


def test_extract_matric_number_removes_spaces():
    assert extract_matric_number("Matric No: CYB / 23U / 4190") == "CYB/23U/4190"


def test_registered_student_card_text_matches(tmp_path):
    repository = StudentRepository(tmp_path / "students.db")
    service = VerificationService(repository)

    result = service.verify_card_text(
        "Name: Moses Thelma Marvellous\nMatric No: CYB/23U/4190\nDepartment: Cyber Security"
    )

    assert result.matched is True
    assert result.student is not None
    assert service.verify_secret_answer(result.student, "2023") is True


def test_unknown_matric_number_is_rejected(tmp_path):
    repository = StudentRepository(tmp_path / "students.db")
    service = VerificationService(repository)

    result = service.verify_card_text("Name: Unknown\nMatric No: CYB/23U/9999\nDepartment: Cyber Security")

    assert result.matched is False
