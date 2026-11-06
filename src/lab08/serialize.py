from src.lab08.models import student_from_dict
from pathlib import Path
import json
import csv


ENCODING = "utf-8"


def students_to_json(students: list[dict], path: str | Path) -> None:
    """
    Serialize students to json.
    json.dump(..., ensure_ascii=False, indent=2)
    """

    json_path = Path(path)
    with json_path.open("w", encoding=ENCODING) as f:
        json.dump(students, f, ensure_ascii=False, indent=2)


def students_from_json(path: str | Path) -> list[dict]:
    """
    Deserialize students from json.

    Strict: raises ValueError if a rec is invalid.
    """
    students = []

    json_path = Path(path)
    with json_path.open(encoding=ENCODING) as f:
        students = json.load(f)

    for i, rec in enumerate(students):
        try:
            students[i] = student_from_dict(rec)
        except (ValueError, TypeError) as err:
            raise ValueError(f"rec {i}: invalid") from err

    return students


def students_from_csv(path: str | Path) -> list[dict]:
    """
    Deserialize students from csv.
    """
    students = []

    csv_path = Path(path)
    with csv_path.open(encoding=ENCODING) as f:
        r = csv.DictReader(f)
        for i, row_dict in enumerate(r):
            try:
                students.append(student_from_dict(row_dict))
            except (ValueError, TypeError) as err:
                raise ValueError(f"rec {i}: invalid") from err

    return students
