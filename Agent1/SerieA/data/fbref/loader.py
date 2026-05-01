# data/fbref/loader.py

import csv
from pathlib import Path


def load_fbref_csv(path: str) -> list[dict]:
    records = []

    with open(Path(path), newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    return records
