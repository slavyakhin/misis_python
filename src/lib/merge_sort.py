from typing import TypeVar, Callable

T = TypeVar("T")


def __merge(
        A: list[T],
        B: list[T],
        key: Callable[[T], object] | None = None,
        reverse: bool = False
) -> list[T]:
    '''return new merged list'''

    if key is None:
        key = lambda x: x

    result = []

    i, j = 0, 0
    while i < len(A) and j < len(B):
        if (key(A[i]) < key(B[j])) != reverse:
            result.append(A[i])
            i += 1
        else:
            result.append(B[j])
            j += 1

    result.extend(A[i:])
    result.extend(B[j:])

    return result
    

def merge_sorted(
        items: list[T],
        key: Callable[[T], object] | None = None,
        reverse: bool = False
) -> list[T]:
    '''
    Sorted copy of list using merge sort
    
    elements (key(element) if key specified) must support '<' operator
    '''

    if len(items) <= 1:
        return items.copy()

    if key is None:
        key = lambda x: x

    mid = len(items) // 2

    A = merge_sorted(items[:mid], key, reverse)
    B = merge_sorted(items[mid:], key, reverse)

    result = __merge(A, B, key, reverse)
    
    return result
