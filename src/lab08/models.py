from datetime import date

STUDENT_FIELDS = {"fio", "birthdate", "group", "gpa"}


def make_student(fio: str, birthdate: str, group: str, gpa: int | float) -> dict:
    """
    Student constructor
    """
    rec = {
        "fio": fio,
        "birthdate": birthdate,
        "group": group,
        "gpa": float(gpa),
    }

    validate_student(rec)

    return rec


def _validate_student_fields(rec: dict) -> None:
    """
    Raise ValueError if any of STUDENT_FIELDS missing
    """
    missing_fields = set(STUDENT_FIELDS) - set(rec.keys())
    if missing_fields:
        raise ValueError(f"no {", ".join(missing_fields)}")


def validate_student(rec: dict) -> None:
    """
    Make sure rec is valid student record.
    """
    
    _validate_student_fields(rec)

    if not isinstance(rec["fio"], str):
        raise TypeError("fio must be string")
    if not rec["fio"].strip():
        raise ValueError("fio is empty")
    fio_list = list(rec["fio"].split())
    if not 2 <= len(fio_list) <= 3:
        raise ValueError("fio must contain 2 or 3 words")

    if not isinstance(rec["birthdate"], str):
        raise TypeError("birthdate must be string")
    try:
        date.fromisoformat(rec["birthdate"]) # Raises ValueError if date is invalid
    except ValueError:
        raise ValueError("invalid birthdate")

    if not isinstance(rec["group"], str):
        raise TypeError("group must be string")
    if not rec["group"].strip():
        raise ValueError("group is empty")

    if not isinstance(rec["gpa"], float | int):
        raise TypeError("gpa must be float or int")
    if not (0 <= rec["gpa"] <= 5):
        raise ValueError("gpa must be in range [0, 5]")

    if rec.keys() != STUDENT_FIELDS:
        raise ValueError("unwanted fields provided")


def student_age(rec: dict, today: date | str | None = None) -> int:
    """
    Get students current age
    """

    if isinstance(today, str):
        today = date.fromisoformat(today)
    if today is None:
        today = date.today()

    birthdate = date.fromisoformat(rec["birthdate"])

    if today < birthdate:
        raise ValueError("not born yet")

    return today.year - birthdate.year - \
            ((today.month, today.day) < (birthdate.month, birthdate.day))


def format_student(rec: dict) -> str:
    """
    Stringer for student rec.
    """

    fio_list = list(rec["fio"].split())
    name = f'{fio_list[0].capitalize()} {"".join(map(lambda x: x[0].upper()+'.', fio_list[1:]))}'

    group = rec["group"].strip()

    age = student_age(rec)

    gpa = rec["gpa"]

    return f'{name} ({group}), {age} лет, GPA {gpa:2f}'


def student_to_dict(rec: dict) -> dict:
    """
    Copy student rec.
    """

    # references to immutable object
    # when new vars are modified, a new objects will be created
    # objects with other references will retain their values
    new_rec = {
        "fio":       rec["fio"],        # str immutable
        "birthdate": rec["birthdate"],  # str immutable
        "group":     rec["group"],      # str immutable
        "gpa":       rec["gpa"],        # float immutable
    }

    return new_rec


def student_from_dict(d: dict) -> dict:
    """
    Deserialization. Pick only necessary fields.
    Copies values.
    Casts types.
    Validates rec.
    """
    _validate_student_fields(d)

    # make_student calls validation
    return make_student(
        str(d["fio"]),
        str(d["birthdate"]),
        str(d["group"]),
        float(d["gpa"]),
    )


def update_student(rec: dict, **fields) -> dict:
    """
    New record with updated fields.
    """
    for key in fields.keys():
        if not key in STUDENT_FIELDS:
            raise KeyError(f"unknown key provided: {key}")

    return make_student(
        fio=        fields.get("fio", rec["fio"]),
        birthdate=  fields.get("birthdate", rec["birthdate"]),
        group=      fields.get("group", rec["group"]),
        gpa=        fields.get("gpa", rec["gpa"]),
    )
