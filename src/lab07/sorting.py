def bubble_sorted(nums) -> list:
    """ sorted list O(n^2).
    """
    nums_new = nums.copy()

    unsorted_count = len(nums_new)
    swapped = True
    while swapped:
        swapped = False
        for i in range(unsorted_count-1):
            if nums_new[i+1] < nums_new[i]:
                nums_new[i], nums_new[i+1] = nums_new[i+1], nums_new[i]
                swapped = True
        unsorted_count -= 1

    return nums_new


def insertion_sorted(nums) -> list:
    """ sorted list O(n^2).
    """
    nums_new = nums.copy()

    for i in range(len(nums_new)):
        for j in range(i, 0, -1):
            if nums_new[j] < nums_new[j-1]:
                nums_new[j], nums_new[j-1] = nums_new[j-1], nums_new[j]
    return nums_new


def selection_sorted(nums) -> list:
    """ sorted list O(n^2).
    """
    nums_new = nums.copy()
    
    sorted_count = 0
    while sorted_count < len(nums_new):
        cur_min_ind = sorted_count
        for i in range(sorted_count, len(nums_new)):
            if nums_new[i] < nums_new[cur_min_ind]:
                cur_min_ind = i
        nums_new[sorted_count], nums_new[cur_min_ind] = nums_new[cur_min_ind], nums_new[sorted_count]
        sorted_count += 1

    return nums_new


def merge_sorted(nums) -> list:
    """ sorted list O(nlong).
    Non recursive version.
    """
    nums_new = nums.copy()

    section_len = 1
    while section_len < len(nums_new):

        for section_a_begin in range(0, len(nums_new), section_len*2):
            section_a_end = min(section_a_begin + section_len, len(nums_new))
            section_b_begin = section_a_end
            section_b_end = min(section_b_begin + section_len, len(nums_new))

            merged_sections = []

            i, j = section_a_begin, section_b_begin
            while i < section_a_end and j < section_b_end:
                if nums_new[i] < nums_new[j]:
                    merged_sections.append(nums_new[i])
                    i += 1
                else:
                    merged_sections.append(nums_new[j])
                    j += 1
            while i < section_a_end:
                merged_sections.append(nums_new[i])
                i += 1
            while j < section_b_end:
                merged_sections.append(nums_new[j])
                j += 1

            for i, value in enumerate(merged_sections):
                nums_new[section_a_begin + i] = value
        
        section_len *= 2

    return nums_new


def counting_sorted(nums, lo, hi) -> list:
    """ sorted list O(n).
    Counts ints from lo to hi inclusive.
    """

    if hi < lo:
        raise ValueError("lo must be less than hi")

    # int is immutable, it's safe to use multiplication operator '*'
    counter = [0] * (hi+1 - lo)
    for value in nums:
        if value < lo or hi < value:
            raise ValueError("nums value not in range [lo, hi]")
        counter[value-lo] += 1

    result = []
    for i, count in enumerate(counter):
        result.extend([i+lo] * count)

    return result
