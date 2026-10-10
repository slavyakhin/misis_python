from src.lib.merge_sort import merge_sorted


def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    '''return tuple of minimum and maximum number in list'''

    if not isinstance(nums, list):
        raise TypeError("nums must be list")
    if not all(type(x) in (int, float) for x in nums):
        raise TypeError("all elements must be int or float")
    if not nums:
        raise ValueError("nums must not be empty")

    cur_min, cur_max = nums[0], nums[0]
    for num in nums:
        if num < cur_min:
            cur_min = num
        if cur_max < num:
            cur_max = num

    return cur_min, cur_max


def unique_sorted(nums: list[float | int]) -> list[float | int]:
    '''return sorted ascending list of unique numbers'''

    if not isinstance(nums, list):
        raise TypeError("nums must be list")
    if not all(type(x) in (int, float) for x in nums):
        raise TypeError("all elements must be int or float")

    # Python has unordered map
    unique_nums = list(set(nums))

    # Sort
    unique_nums = merge_sorted(unique_nums)

    return unique_nums


def flatten(mat: list[list | tuple]) -> list:
    '''serialized matrix'''

    if not isinstance(mat, list):
        raise TypeError("mat must be list")
    if not all(type(x) in (list, tuple) for x in mat):
        raise TypeError("all elements must be list or tuple")

    result = []
    for row in mat:
        for element in row:
            result.append(element) # any type allowed

    return result
