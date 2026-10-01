import pytest
from src.lab02.tuples import format_record

# --------------- format_record ---------------
# --------------- Default tests ---------------
@pytest.mark.parametrize(
    "a, expected",
    [
        (("Иванов Иван Иванович", "BIVT-25", 4.6), "Иванов И.И., гр. BIVT-25, GPA 4.60"),
        (("Петров Пётр", "IKBO-12", 5.0), "Петров П., гр. IKBO-12, GPA 5.00"),
        (("Петров Пётр Петрович", "IKBO-12", 5.0), "Петров П.П., гр. IKBO-12, GPA 5.00"),
        ((" сидорова анна сергеевна ", "ABB-01", 3.999), "Сидорова А.С., гр. ABB-01, GPA 4.00"),
    ],
)
def test_format_record(a, expected):
    assert format_record(a) == expected

# --------------- Custom tests ---------------
@pytest.mark.parametrize(
    "a, expected",
    [
        ((" сидОроВа аННа сергеевна ", "   ABB-01   ", 3.999), "Сидорова А.С., гр. ABB-01, GPA 4.00"),
    ],
)
def test_additional_format_record(a, expected):
    assert format_record(a) == expected

@pytest.mark.parametrize(
    "a",
    [
        [],
        {},
        123,
        ((),(),()),
        (1, 1, 1),
        ("str", "abc", "abacaba"),
        ("str", "abacaba", 4), # int gpa
    ]
)
def test_additonal_format_record_invalid_types(a):
    with pytest.raises(TypeError):
        format_record(a)

@pytest.mark.parametrize(
    "a",
    [
        ("str", "abacaba", 4.0), # one word fio
        ("", "group", 4.0),
        ("name surname", "", 4.0),
        ("name surname lastanme fame lame same game", "", 4.0),
    ]
)
def test_additonal_format_record_invalid_values(a):
    with pytest.raises(ValueError):
        format_record(a)

