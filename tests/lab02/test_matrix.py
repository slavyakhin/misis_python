import pytest
from src.lab02.matrix import transpose, row_sums, col_sums


# ----------------- transpose -----------------
# --------------- Default tests ---------------
@pytest.mark.parametrize(
    "a, expected",
    [
        ([[1, 2, 3]], [[1], [2], [3]]),
        ([[1], [2], [3]], [[1, 2, 3]]),
        ([[1, 2], [3, 4]], [[1, 3], [2, 4]]),
        ([], []),
    ],
)
def test_transpose(a, expected):
    assert transpose(a) == expected

def test_transpose_jagged_array():
    with pytest.raises(ValueError):
        transpose([[1, 2], [3]])

# --------------- Custom tests ---------------
@pytest.mark.parametrize(
    "a",
    [
        "string",
        (),
        ["string", 42],        
    ],
)
def test_additional_transpose_invalid_type(a):
    with pytest.raises(TypeError):
        transpose(a)


# ----------------- row_sums ------------------
# --------------- Default tests ---------------
@pytest.mark.parametrize(
    "a, expected",
    [
        ([[1, 2, 3], [4, 5, 6]], [6, 15]),
        ([[-1, 1], [10, -10]], [0, 0]),
        ([[0, 0], [0, 0]], [0, 0]),
    ],
)
def test_row_sums(a, expected):
    assert row_sums(a) == expected

def test_row_sums_jagged_array():
    with pytest.raises(ValueError):
        row_sums([[1, 2], [3]])

# --------------- Custom tests ---------------
@pytest.mark.parametrize(
    "a",
    [
        "string",
        (),
        ["string", 42],        
    ],
)
def test_additional_row_sums_invalid_type(a):
    with pytest.raises(TypeError):
        row_sums(a)


# ----------------- col_sums ------------------
# --------------- Default tests ---------------
@pytest.mark.parametrize(
    "a, expected",
    [
        ([[1, 2, 3], [4, 5, 6]], [5, 7, 9]),
        ([[-1, 1], [10, -10]], [9, -9]),
        ([[0, 0], [0, 0]], [0, 0]),
    ]
)
def test_col_sums(a, expected):
    assert col_sums(a) == expected

def test_col_sums_jagged_array():
    with pytest.raises(ValueError):
        col_sums([[1, 2], [3]])

# --------------- Custom tests ---------------
@pytest.mark.parametrize(
    "a",
    [
        "string",
        (),
        ["string", 42],        
    ],
)
def test_additional_col_sums_invalid_type(a):
    with pytest.raises(TypeError):
        col_sums(a)
