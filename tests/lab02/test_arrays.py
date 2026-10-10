import pytest
from src.lab02.arrays import min_max, unique_sorted, flatten


# ------------------ min_max ------------------
# --------------- Default tests ---------------
@pytest.mark.parametrize(
        "a, expected",
        [
            ([3, -1, 5, 5, 0], (-1, 5)),
            ([42], (42, 42)),
            ([-5, -2, -9], (-9, -2)),
            ([1.5, 2, 2.0, -3.1], (-3.1, 2)),
        ],
)
def test_min_max(a, expected):
    assert min_max(a) == expected

def test_min_max_empty_list():
    with pytest.raises(ValueError):
        min_max([])

# --------------- Custom tests ---------------
@pytest.mark.parametrize(
        "a, expected",
        [
            ([0, 0], (0, 0)),
            ([1e27], (1e27, 1e27)),
            ([1e27, 1e-27, -1e27], (-1e27, 1e27)),
        ],
)
def test_additional_min_max(a, expected):
    assert min_max(a) == expected

@pytest.mark.parametrize(
        "a",
        [
            "string",
            1.846,
            85,
            {},
            (),
            ["str", 1.12, {}, [[[]]]],
        ],
)
def test_additional_min_max_invalid_types(a):
    with pytest.raises(TypeError):
        min_max(a)


@pytest.mark.parametrize(
        "a",
        [
            42,
            "abacaba",
            (42, "abacaba"),
            {},
        ],
)
def  test_additional_min_max_wrong_type(a):
    with pytest.raises(TypeError):
        min_max(a)


# --------------- unique_sorted ---------------
# --------------- Default tests ---------------
@pytest.mark.parametrize(
        "a, expected",
        [
            ([3, 1, 2, 1, 3], [1, 2, 3]),
            ([], []),
            ([-1, -1, 0, 2, 2], [-1, 0, 2]),
            ([1.0, 1, 2.5, 2.5, 0], [0, 1.0, 2.5]),
        ],
)
def test_unique_sorted(a, expected):
    assert unique_sorted(a) == expected

# --------------- Custom tests ---------------
@pytest.mark.parametrize(
        "a, expected",
        [
            ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
            ([5, 5.0, 5, 2, 1], [1, 2, 5]),
            ([0, 0, 0], [0]),
            ([0.0, 0.0, 0], [0]),
        ],
)
def test_additional_unique_sorted(a, expected):
    assert unique_sorted(a) == expected

@pytest.mark.parametrize(
        "a",
        [
            42,
            "abacaba",
            (42, "abacaba"),
            {},
        ],
)
def  test_additional_unique_sorted_wrong_type(a):
    with pytest.raises(TypeError):
        unique_sorted(a)


# ------------------ flatten ------------------
# --------------- Default tests ---------------
@pytest.mark.parametrize(
        "a, expected",
        [
            ([[1, 2], [3, 4]], [1, 2, 3, 4]),
            ([[1, 2], (3, 4, 5)], [1, 2, 3, 4, 5]),
            ([[1], [], [2, 3]], [1, 2, 3]),
        ],
)
def test_flatten(a, expected):
    # Minimum tests
    assert flatten(a) == expected

def test_flatten_wrong_type():
    with pytest.raises(TypeError):
        flatten([[1, 2], "ab"]) # type: ignore

# --------------- Custom tests ---------------
@pytest.mark.parametrize(
        "a, expected",
        [
            ([], []),
            ([[]], []),
        ],
)
def test_additional_flatten(a, expected):
    # Minimum tests
    assert flatten(a) == expected

@pytest.mark.parametrize(
        "a",
        [
            42,
            "abacaba",
            (42, "abacaba"),
            {},
        ],
)
def  test_additional_flatten_wrong_type(a):
    with pytest.raises(TypeError):
        flatten(a)


