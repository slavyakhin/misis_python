import csv
from pathlib import Path
from src.lib.text import normalize
from src.lib.search import key_index
from src.lab08.models import STUDENT_FIELDS, student_from_dict, validate_student, update_student as model_update_student


ENCODING="utf-8"


def ensure_storage(path: str | Path) -> None:
    """
    Create file with header if not exist.

    Creates parent dirs.
    """

    path = Path(path)

    if path.suffix != ".csv":
        raise ValueError('file extensoin must be ".csv"')

    if path.exists():
        return

    # No such file => create with headers

    # Ensure parent dir.
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding=ENCODING) as f:
        f.write(','.join(STUDENT_FIELDS))


def  load_students(path: str | Path) -> list[dict]:
    """
    Read all recs from csv.
    """

    path = Path(path)

    if path.suffix != ".csv":
        raise ValueError('file extensoin must be ".csv"')

    with path.open(encoding=ENCODING) as f:
        r = csv.DictReader(f)

        if r.fieldnames is None:
            raise ValueError("no fieldnames in csv")
        if dict.fromkeys(r.fieldnames) != STUDENT_FIELDS:
            raise ValueError("csv fieldnames do not match student rec")

        l = list(map(student_from_dict, r))

    return l


def save_students(path: str | Path, students: list[dict]) -> None:
    """
    Write students to csv.

    Rewrites file.
    """

    if not isinstance(students, list) or not all(isinstance(rec, dict) for rec in students):
        raise TypeError("students must be list[dict]")

    path = Path(path)

    ensure_storage(path)

    # newline="" crucial for writing csv in windows to avoid double blank lines
    with path.open("w", newline="", encoding=ENCODING) as f:
        w = csv.DictWriter(f, fieldnames=STUDENT_FIELDS)
        w.writeheader()
        w.writerows(students)


def add_student(path: str | Path, student: dict) -> None:
    """
    Append student to csv.

    Raises ValuError if a student with given fio exists

    Validates student.
    """

    students = load_students(path)

    validate_student(student)

    if any(s["fio"] == student["fio"] for s in students):
        raise ValueError("fio exists")

    students.append(student)

    save_students(path, students)


def list_students(path: str | Path, sort_by: str | None=None) -> list[dict]:
    """
    List of students.

    sort_by {None, "fio", "gpa"}
    """

    if not isinstance(sort_by, str | None):
        raise TypeError("sort_by must be str | None")

    students = load_students(path)

    match sort_by:
        case None:
            pass
        case "fio":
            students.sort(key=(lambda s: s["fio"]))
        case "gpa":
            students.sort(key=(lambda s: s["gpa"]), reverse=True)
        case _:
            raise ValueError('unknonwn "sort_by"')

    return students


def find_students(path: str | Path, substr: str) -> list[dict]:
    """
    List of students with substr substring in fio.

    Case-insensitive.
    """

    if not isinstance(substr, str):
        raise TypeError("substr must be string")

    students = load_students(path)

    substr = normalize(substr)

    substr_students = []
    for student in students:
        if substr in normalize(student["fio"]):
            substr_students.append(student)

    return substr_students


def update_student(path: str | Path, fio: str, **fields) -> bool:
    """
    Update first occurence with given fio.

    Case sensitive.

    Return whether occurence has been found.
    """

    if not isinstance(fio, str):
        raise TypeError("fio must be string")

    students = load_students(path)

    # search
    try:
        ind = key_index(students, fio, lambda rec, fio: rec["fio"] == fio)
    except ValueError:
        return False

    new_student = model_update_student(students[ind], **fields)

    students = students[:ind] + [new_student] + students[ind+1:]

    save_students(path, students)

    return True


def remove_students(path: str | Path, fio: str) -> int:
    """
    Remove all recs with given fio.
    
    Return number of deleted recs.

    Case sensitive.
    """

    if not isinstance(fio, str):
        raise TypeError("fio must be string")

    students = load_students(path)

    new_students = [rec for rec in students if rec["fio"] != fio]

    save_students(path, new_students)

    return len(students) - len(new_students)


def stats(path: str | Path) -> dict:
    """
    {
        "count": total students count,
        "min_gpa": min gpa,
        "max_gpa": max gpa,
        "avg_gpa": avg gpa,
        "groups": {
            "БИВТ-26-6-1": students count,
            "БИВТ-26-6-2": students count,
            ...
        },
        "top_5_students": [
            {"fio": "...", "gpa": ...},
            ...
        ]
    }
    """

    students = list_students(path, sort_by="gpa")

    d = dict()

    d["count"] = len(students)
    d["min_gpa"] = students[-1]["gpa"]
    d["max_gpa"] = students[0]["gpa"]

    groups = dict()
    for s in students:
        groups[s["group"]] = groups.get(s["group"], 0) + 1

    groups = dict(sorted(groups.items()))

    d["groups"] = groups

    d[f"top_{len(students) if len(students) < 5 else 5}_students"] = students[:5]

    return d
