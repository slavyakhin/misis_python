def transpose(mat: list[list[float | int]]) -> list[list]:
    '''return transposed matrix'''

    if not isinstance(mat, list):
        raise TypeError("mat must be list")
    if not mat:
        return []

    if not all(isinstance(x, list) for x in mat):
        raise TypeError("all elements must be list (rows)")
    if not all(len(row) == len(mat[0]) for row in mat):
        raise ValueError("all rows must be same length")
    if not all( all(type(x) in (float, int) for x in row) for row in mat):
        raise TypeError("all matrix elements must be int or float")

    result = [ [mat[i][j] for i in range(len(mat))]
              for j in range(len(mat[0])) ]

    return result


def row_sums(mat: list[list[float | int]]) -> list[float]:
    '''return list, each element is sum of row elements'''

    if not isinstance(mat, list):
        raise TypeError("mat must be list")
    if not mat:
        return []

    if not all(isinstance(x, list) for x in mat):
        raise TypeError("all elements must be list (rows)")
    if not all(len(row) == len(mat[0]) for row in mat):
        raise ValueError("all rows must be same length")
    if not all( all(type(x) in (float, int) for x in row) for row in mat):
        raise TypeError("all matrix elements must be int or float")

    # list[float]
    result = [ 0.0 for _ in range(len(mat)) ]

    for i, row in enumerate(mat):
        for element in row:
            result[i] += float(element)

    return result


def col_sums(mat: list[list[float | int]]) -> list[float]:
    '''return list, each element is sum of column elements'''

    if not isinstance(mat, list):
        raise TypeError("mat must be list")
    if not mat:
        return []

    if not all(isinstance(x, list) for x in mat):
        raise TypeError("all elements must be list (rows)")
    if not all(len(row) == len(mat[0]) for row in mat):
        raise ValueError("all rows must be same length")
    if not all( all(type(x) in (float, int) for x in row) for row in mat):
        raise TypeError("all matrix elements must be int or float")

    # list[float]
    result = [ 0.0 for _ in range(len(mat[0]))]

    for row in mat:
        for j, element in enumerate(row):
            result[j] += float(element)

    return result
