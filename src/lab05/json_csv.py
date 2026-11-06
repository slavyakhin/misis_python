import json, csv
from pathlib import Path
from src.lab02.arrays import flatten

ENCODING = "utf-8"


def json_to_csv(json_path: str | Path, csv_path: str | Path) -> None:
    """
    Convert JSON into CSV.

    Supports list of dicts [{...}, {...}], fills missing fields with empty strings.\n
    Encoding UTF-8. Keys(columns) order - same as in input.
    """

    json_path = Path(json_path)

    if json_path.suffix != ".json":
        raise ValueError('json file must have ".json" extenstion')

    csv_path = Path(csv_path)

    if csv_path.suffix != ".csv":
        raise ValueError('csv file must have ".csv" extenstion')


    with json_path.open(encoding=ENCODING) as f:
        data = json.load(f)

    if not data:
        raise ValueError("Empty JSON or unsupported structure")
    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list")
    if not all(isinstance(x, dict) for x in data):
        raise ValueError("All input list elements must be a dict")

    # dict.fromkeys provides uniqueness, preserving order
    # flatten isn't polymorphic, we forced to cast to list
    headers = dict.fromkeys(
            flatten(list(
            list(d.keys()) for d in data
            )))

    with csv_path.open("w", encoding=ENCODING) as f:
        w = csv.DictWriter(f, headers)
        w.writeheader()
        w.writerows(data)


def csv_to_json(csv_path: str | Path, json_path: str | Path) -> None:
    """
    Convert CSV into JSON (list of dicts).

    Header is mandatory, values stored as strings.
    json.dump(..., ensure_ascii=False, indent=2)
    """

    csv_path = Path(csv_path)

    if csv_path.suffix != ".csv":
        raise ValueError('csv file must have ".csv" extenstion')

    json_path = Path(json_path)

    if json_path.suffix != ".json":
        raise ValueError('json file must have ".json" extenstion')


    with csv_path.open(encoding=ENCODING) as f:
        r = csv.DictReader(f) # fieldnames omitted, so first row values must be fieldnames

        if not r.fieldnames:
            raise ValueError("No fieldnames in csv.")

        if not any(r.fieldnames):
            raise ValueError("Empty fieldnames in csv.")

        data = list(r) # list of dicts

    if not data:
        raise ValueError("Empty csv or missing column names")

    with json_path.open("w", encoding=ENCODING) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
