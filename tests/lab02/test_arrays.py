import pytest
from src.lab02.arrays import min_max, unique_sorted, flatten


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

    with pytest.raises(ValueError):
        min_max([])


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

    with pytest.raises(TypeError):
        flatten([[1, 2], "ab"]) # type: ignore
