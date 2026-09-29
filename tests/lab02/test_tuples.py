import pytest
from src.lab02.tuples import format_record

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
