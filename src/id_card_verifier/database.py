"""SQLite storage for registered student records."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import Student

DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "data" / "students.db"

SAMPLE_STUDENTS = (
    Student(
        matric_number="CYB/23U/4190",
        full_name="Moses Thelma Marvellous",
        department="Cyber Security",
        faculty="Computing",
        admission_year="2023",
        level="300",
        secret_answer="2023",
    ),
    Student(
        matric_number="CSC/22U/1001",
        full_name="Aisha Ibrahim",
        department="Computer Science",
        faculty="Computing",
        admission_year="2022",
        level="400",
        secret_answer="2022",
    ),
    Student(
        matric_number="IFT/24U/2048",
        full_name="Daniel Okoro",
        department="Information Technology",
        faculty="Computing",
        admission_year="2024",
        level="200",
        secret_answer="2024",
    ),
)


class StudentRepository:
    """Small repository wrapper around the SQLite student database."""

    def __init__(self, db_path: Path | str = DEFAULT_DB_PATH) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_schema()
        self.seed_defaults()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _create_schema(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    matric_number TEXT PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    faculty TEXT NOT NULL,
                    admission_year TEXT NOT NULL,
                    level TEXT NOT NULL,
                    secret_answer TEXT NOT NULL
                )
                """
            )

    def seed_defaults(self) -> None:
        """Insert demo records so the application works immediately after cloning."""

        with self._connect() as connection:
            connection.executemany(
                """
                INSERT OR IGNORE INTO students (
                    matric_number,
                    full_name,
                    department,
                    faculty,
                    admission_year,
                    level,
                    secret_answer
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        student.matric_number,
                        student.full_name,
                        student.department,
                        student.faculty,
                        student.admission_year,
                        student.level,
                        student.secret_answer,
                    )
                    for student in SAMPLE_STUDENTS
                ],
            )

    def all_students(self) -> list[Student]:
        """Return all registered students ordered by matric number."""

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT matric_number, full_name, department, faculty,
                       admission_year, level, secret_answer
                FROM students
                ORDER BY matric_number
                """
            ).fetchall()
        return [self._row_to_student(row) for row in rows]

    def find_by_matric(self, matric_number: str) -> Student | None:
        """Look up a student by matriculation number."""

        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT matric_number, full_name, department, faculty,
                       admission_year, level, secret_answer
                FROM students
                WHERE UPPER(matric_number) = UPPER(?)
                """,
                (matric_number.strip(),),
            ).fetchone()
        return self._row_to_student(row) if row else None

    @staticmethod
    def _row_to_student(row: sqlite3.Row) -> Student:
        return Student(
            matric_number=row["matric_number"],
            full_name=row["full_name"],
            department=row["department"],
            faculty=row["faculty"],
            admission_year=row["admission_year"],
            level=row["level"],
            secret_answer=row["secret_answer"],
        )
