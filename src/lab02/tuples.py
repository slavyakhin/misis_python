# Python 3.12 PEP695 type alias (fio: str, group: str, gpa: float)
type Rec = tuple[str, str, float]

def format_record(rec: Rec) -> str:
    '''returns formatted string e.g. "Иванов И.И., гр. BIVT-25, GPA 4.60"'''

    if not isinstance(rec, tuple):
        raise TypeError("rec must be tuple")
    if not (len(rec) == 3 and
            (list(map(type, rec)) == [str, str, float])):
        raise TypeError("rec elements must be [str, str, float]")

    fio_list = rec[0].split()
    if len(fio_list) < 2 or 3 < len(fio_list):
        raise ValueError("fio must contain 2 or 3 words")

    fio_str = fio_list[0][0].upper() + fio_list[0][1:].lower() + ' ' + ''.join(name[0].upper() + '.' for name in fio_list[1:])

    return f'{fio_str}, гр. {rec[1].strip()}, GPA {rec[2]:.2f}'
