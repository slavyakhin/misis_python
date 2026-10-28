def linear_search(nums, x):
    """First occurrence index x or -1.
 
    linear_search([4, 2, 7, 2], 2) -> 1
    linear_search([4, 2, 7, 2], 9) -> -1
    linear_search([], 1) -> -1
    """

    for i, num in enumerate(nums):
        if num == x:
            return i

    return -1
 
 
def binary_search(sorted_nums, x):
    """Index of x in ascending list or -1.
    Find first occurence.
    Undefined behaviour on unsorted list
 
    binary_search([1, 3, 5, 7], 5) -> 2
    binary_search([1, 3, 5, 7], 4) -> -1
    binary_search([5], 5) -> 0
    binary_search([], 5) -> -1
    """

    # TODO: find first occurence [-95, -95, 88] -> 0
    if not sorted_nums:
        return -1

    l, r = 0, len(sorted_nums)
    while (l < r):
        m = (l+r) // 2
        if sorted_nums[m] < x:
            l = m + 1
        else:
            r = m
    if l < len(sorted_nums) and sorted_nums[l] == x:
        return l
    return -1

 
def two_sum_brute(nums, target):
    """Pair of indexes (i, j), i < j, nums[i] + nums[j] == target, or None.
 
    two_sum_brute([2, 7, 11, 15], 9) -> (0, 1)
    two_sum_brute([1, 2], 10) -> None
    """

    for i in range(len(nums)-1):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)

    return None

 
def two_sum_fast(nums, target):
    """Pair of indexes (i, j), i < j, nums[i] + nums[j] == target, or None.

    two_sum_fast([2, 7, 11, 15], 9) -> (0, 1)
    two_sum_fast([1, 2], 10) -> None
    """
    
    # index of value that forms required pair with the given value
    complements_inds = dict()

    for j in range(len(nums)):
        if nums[j] in complements_inds:
            return (complements_inds[nums[j]], j)
        complements_inds[target - nums[j]] = j

    return None
