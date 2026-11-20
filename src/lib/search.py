from typing import TypeVar, Callable, Sequence


T_A = TypeVar("T_A")
T_B = TypeVar("T_B")


def key_index(l: Sequence[T_A], value: T_B, key: Callable[[T_A, T_B], bool]) -> int:
    """
    Return first index of value.

    Raises ValueError if the value is not present.
    """

    for i, elem in enumerate(l):
        if key(elem, value):
            return i

    raise ValueError("mathcing value not found")
