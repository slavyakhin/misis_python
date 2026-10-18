import json, csv
from pathlib import Path
from src.lab02.arrays import flatten

ENCODING = "utf-8"


def json_to_csv(json_path: str, csv_path: str) -> None:
    """
    Convert JSON into CSV.

    Supports list of dicts [{...}, {...}], fills missing fields with empty strings.\n
    Encoding UTF-8. Keys(columns) order - same as in input.
    """

    json_path_path = Path(json_path)
    with json_path_path.open(encoding=ENCODING) as f:
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

    csv_path_path = Path(csv_path)
    with csv_path_path.open("w", encoding=ENCODING) as f:
        w = csv.DictWriter(f, headers)
        w.writeheader()
        w.writerows(data)


def csv_to_json(csv_path: str, json_path: str) -> None:
    """
    Convert CSV into JSON (list of dicts).

    Header is mandatory, values stored as strings.
    json.dump(..., ensure_ascii=False, indent=2)
    """

    csv_path_path = Path(csv_path)
    with csv_path_path.open(encoding=ENCODING) as f:
        r = csv.DictReader(f) # fieldnames omitted, so first row values must be fieldnames
        data = list(r) # list of dicts

    if not data:
        raise ValueError("Empty csv or missing column names")

    json_path_path = Path(json_path)
    with json_path_path.open("w", encoding=ENCODING) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
