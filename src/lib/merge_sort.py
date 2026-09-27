def __merge(A: list[int | float], B: list[int | float]) -> list[int | float]:
    '''return new merged list'''

    result = []

    i, j = 0, 0
    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            result.append(A[i])
            i += 1
        else:
            result.append(B[j])
            j += 1

    while i < len(A):
        result.append(A[i])
        i += 1

    while j < len(B):
        result.append(B[j])
        j += 1

    return result
    

def __merge_sort(nums: list[int | float]) -> list[int | float]:
    '''returns sorted copy of nums'''

    if len(nums) < 2:
        return nums.copy()
    if len(nums) == 2:
        if nums[1] < nums[0]:
            return [nums[1], nums[0]]
        return nums.copy()

    A = __merge_sort(nums[:len(nums) // 2]) # slice copies
    B = __merge_sort(nums[len(nums) // 2:]) # slice copies

    result = __merge(A, B)

    return result


def merge_sorted(nums: list[int | float]) -> list[int | float]:
    '''returns sorted copy of list, using merge sort'''

    if not isinstance(nums, list):
        raise TypeError("nums must be list")
    if not all(type(x) in (int, float) for x in nums):
        raise TypeError("all elements must be int or float")

    return __merge_sort(nums)
