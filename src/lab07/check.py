import random
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort, merge_sort, counting_sort
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast 
 
def check_sorting(fn, trials=100) -> None:
    """
    Generate and complete {trials} tests for a sorting
    """

    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        original = list(nums)
        result = fn(nums)
        assert result == sorted(nums), f"{fn.__name__} ошиблась на {nums}: {result}"
        assert nums == original, f"{fn.__name__} изменила исходный список"


def check_counting_sort(fn, trials=100) -> None:
    """
    Generate and complete {trials} tests for counting sort
    """

    for _ in range(trials):
        n = random.randint(0, 50)
        lo, hi = -100, 100
        nums = [random.randint(lo, hi) for _ in range(n)]
        original = list(nums)
        result = fn(nums, lo, hi)
        assert result == sorted(nums), f"{fn.__name__} ошиблась на {nums}: {result}"
        assert nums == original, f"{fn.__name__} изменила исходный список"


def check_search(fn, trials=100) -> None:
    """
    Generate and complete {trials} tests for a search
    """

    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        nums.sort()

        if not n == 0:
            x = random.choice((nums[random.randint(0, n-1)], 150))
        else:
            x = 150

        result = fn(nums, x)
        try:
            index_result = nums.index(x)
        except ValueError: # not in list
            index_result = -1
        assert result == index_result, f"{fn.__name__} ошиблась на {nums}, {x}: {result}"


def check_two_sum(trials=100) -> None:
    """
    Generate and complete {trials} tests for a two sum solution
    """

    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        i, j = random.randint(0, n-1), random.randint(0, n-1)
        su = random.choice((nums[i] + nums[j], 201))

        result_brute = two_sum_brute(nums, su)
        result_fast = two_sum_fast(nums, su)

        assert (result_brute is None and result_fast is None) \
             or (result_brute is not None and result_fast is not None \
                 and nums[result_brute[0]] + nums[result_brute[1]] == nums[result_fast[0]] + nums[result_fast[1]]), f"результаты не совпадают на {nums}: {result_brute} != {result_fast}"


def main():
    random.seed(42)
    for fn in (bubble_sort, insertion_sort, selection_sort, merge_sort):
        check_sorting(fn)
    check_counting_sort(counting_sort)

    for fn in (linear_search, binary_search):
        check_search(fn)

    # Compares two_sum_brute and two_sum_fast
    check_two_sum()
    
    print("OK")


if __name__ == "__main__":
    main()
