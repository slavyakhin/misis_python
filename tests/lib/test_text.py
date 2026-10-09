import pytest
from src.lib.text import normalize, tokenize, count_freq, top_n

# --------------- normalize ---------------
# ------------- Default tests -------------
@pytest.mark.parametrize(
    "a, expected",
    [
        ("ПрИвЕт\nМИр\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\r\nWorld", "hello world"),
        (" двойные пробелы ", "двойные пробелы"),
    ],
)
def test_normalize(a, expected):
    assert normalize(a) == expected


# ------------- Custom tests --------------
@pytest.mark.parametrize(
    "a, expected",
    [
        ("ёжик, Ёлка", "ёжик, ёлка"),
    ],
)
def test_normalize_no_yo2e(a, expected):
    assert normalize(a, yo2e=False) == expected



# --------------- tokenize ---------------
# ------------- Default tests -------------
@pytest.mark.parametrize(
    "a, expected",
    [
        ("привет мир", ["привет", "мир"]),
        ("hello,world!!!", ["hello", "world"]),
        ("по-настоящему круто", ["по-настоящему", "круто"]),
        ("2025 год", ["2025", "год"]),
        ("emoji 😀 не слово", ["emoji", "не", "слово"]),
    ],
)
def test_tokenize(a, expected):
    assert tokenize(a) == expected


# ------------- Custom tests --------------


# --------------- count_freq ---------------
# ------------- Default tests -------------
@pytest.mark.parametrize(
    "a, expected",
    [
        (["a","b","a","c","b","a"], {"a":3,"b":2,"c":1}),
        (["bb","aa","bb","aa","cc"], {"aa":2,"bb":2,"cc":1}),
    ],
)
def test_count_freq(a, expected):
    assert count_freq(a) == expected


# ------------- Custom tests --------------


# --------------- top_n ---------------
# ------------- Default tests -------------
@pytest.mark.parametrize(
    "a, n, expected",
    [
        ({"a":3,"b":2,"c":1}, 2, [("a", 3), ("b", 2)]),
        ({"aa":2,"bb":2,"cc":1}, 2, [("aa", 2), ("bb", 2)]),
    ],
)
def test_top_n(a, n, expected):
    assert top_n(a, n=n) == expected


# ------------- Custom tests --------------
