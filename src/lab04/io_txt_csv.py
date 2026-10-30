from collections.abc import Sequence
from pathlib import Path, PurePath
import csv

ENCODING = "utf-8"


def read_text(path: str | Path, encoding: str = ENCODING)-> str:
    '''
    String of all chars in file including spaces.

    You may choose encoding with keyword argument
    e.g. encoding="cp1251"
    '''

    # Path is platform-specific, but inherits from PurePath
    # Union operator, pipe symbol `|` in `isinstance` valid in python 3.10+
    if not isinstance(path, str | PurePath):
        raise TypeError("path must be string or Path")
    if not isinstance(encoding, str):
        raise TypeError("encoding must be string")

    p = Path(path)
    # FileNotFoundError and UnicodeDecodeError raises as in task
    result_str = p.read_text(encoding=encoding)

    return result_str


def write_csv(rows: Sequence[tuple | list], path: str | Path, header: tuple[str, ...] | None = None) -> None:
    '''
    Create or rewrite csv file.

    Creates parent dirs if they do not exist.
    '''

    if not all(isinstance(row, tuple | list) for row in rows):
        raise TypeError("rows must be Sequence[tuple | list]")
    if not isinstance(path, str | PurePath):
        raise TypeError("path must be string or Path")
    if header is not None and (not isinstance(header, tuple) or not all(isinstance(s, str) for s in header)):
        raise TypeError("header must be tuple[str | ...]")

    if len(rows) > 0 and not all(len(row) == len(rows[0]) for row in rows):
            raise ValueError("rows must be same length")

    p = Path(path)

    # Ensure parent dirs exist
    p.parent.mkdir(parents=True, exist_ok=True)
    

    # `with` is a syntax sugar for RAII. Replaces `try ... finally` construction
    # open "w", creates new file if it not exist
    # erase file contents if exist
    with p.open("w", newline="", encoding=ENCODING) as file:
        w = csv.writer(file)
        if header is not None:
            w.writerow(header)
        for row in rows:
            w.writerow(row)

    return
