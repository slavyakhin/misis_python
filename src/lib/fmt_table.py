from collections.abc import Sequence

def print_table(rows: Sequence[Sequence]) -> None:
    """
    Print table using f-strings

    rows must be same length.
    """

    if not rows:
        return

    if not isinstance(rows, list) or not all(isinstance(row, tuple | list) for row in rows):
        raise TypeError("rows must be list[tuple | list]")

    if not all(len(row) == len(rows[0]) for row in rows):
        raise ValueError("rows must be same length")

    # find widths of columns
    widths = [0] * len(rows[0])
    for row in rows:
        for i, v in enumerate(row):
            widths[i] = max(widths[i], len(str(v)))

    print(f"┌─{'─┬─'.join('─' * width for width in widths)}─┐")
    print(f"│ {' │ '.join(f'{value:^{widths[i]}}' for i, value in enumerate(rows[0]))} │")
    for row in rows[1:]:
        print(f"├─{'─┼─'.join('─' * width for width in widths)}─┤")
        print(f"│ {' │ '.join(f'{value:^{widths[i]}}' for i, value in enumerate(row))} │")
    print(f"└─{'─┴─'.join('─' * width for width in widths)}─┘")
