"""Data access layer. Loads the people 'table' from CSV."""
from functools import lru_cache
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "people.csv"


@lru_cache(maxsize=1)
def load_people() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    return df


def filter_people(
    min_age: int | None = None,
    max_age: int | None = None,
) -> pd.DataFrame:
    df = load_people()
    if min_age is not None:
        df = df[df["age"] >= min_age]
    if max_age is not None:
        df = df[df["age"] <= max_age]
    return df.reset_index(drop=True)
