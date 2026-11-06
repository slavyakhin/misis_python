from collections.abc import Sequence


def recs_to_rows(recs: list[dict], header: list | None = None) -> list[list]:
    """
    Convert list[dict] table to list[list] table.

    Keys are first row.
    """

    if header is None:
        header = list(dict.fromkeys([key for d in recs for key in d.keys()]))

    rows = [header]
    for rec in recs:
        rows.append([ rec.get(header[i], "-") for i in range(len(header)) ])

    return rows


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
