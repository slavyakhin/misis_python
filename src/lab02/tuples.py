# Python 3.12 PEP695 type alias (fio: str, group: str, gpa: float)
type Rec = tuple[str, str, float]

def format_record(rec: Rec) -> str:
    '''returns formatted string
    
    e.g. "Иванов И.И., гр. BIVT-25, GPA 4.60"
    
    blank fio/group -> ValueError \n
    least words in fio -> ValueError \n
    gpa not in range -> ValueError \n'''

    if not isinstance(rec, tuple):
        raise TypeError("rec must be tuple")
    if len(rec) != 3:
        raise TypeError("rec len must be 3")
    if not isinstance(rec[0], str):
        raise TypeError("fio must be string")
    if not isinstance(rec[1], str):
        raise TypeError("group must be string")
    if not isinstance(rec[2], float):
        raise TypeError("gpa must be float")

    fio_list = rec[0].split()
    if len(fio_list) < 2 or 3 < len(fio_list):
        raise ValueError("fio must contain 2 or 3 words")

    group_str = rec[1].strip()
    if group_str == "":
        raise ValueError("group must not be blank")

    if rec[2] <= 0.0 or 5.5 <= rec[2]:
        raise ValueError("gpa must be in [0.0, 5.0]")


    fio_list = rec[0].split()
    if len(fio_list) < 2 or 3 < len(fio_list):
        raise ValueError("fio must contain 2 or 3 words")

    fio_str = fio_list[0].capitalize() + ' ' + ''.join(name[0].upper() + '.' for name in fio_list[1:])

    return f'{fio_str}, гр. {group_str}, GPA {rec[2]:.2f}'
