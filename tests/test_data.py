"""Unit tests for the data layer."""
import time

import pytest

from app.data import filter_people, load_people


def test_load_people_has_100_rows() -> None:
    df = load_people()
    assert len(df) == 100


def test_load_people_columns() -> None:
    df = load_people()
    assert list(df.columns) == [
        "person_id",
        "age",
        "state",
        "first_name",
        "last_name",
    ]


def test_filter_no_filters_returns_all() -> None:
    assert len(filter_people()) == 100


def test_filter_min_age() -> None:
    df = filter_people(min_age=30)
    assert (df["age"] >= 30).all()


def test_filter_max_age() -> None:
    df = filter_people(max_age=40)
    assert (df["age"] <= 40).all()


def test_filter_min_and_max_age() -> None:
    df = filter_people(min_age=21, max_age=35)
    assert (df["age"] >= 21).all()
    assert (df["age"] <= 35).all()


def test_filter_empty_when_out_of_range() -> None:
    df = filter_people(min_age=200)
    assert df.empty


@pytest.mark.slow
def test_repeated_filter_does_not_mutate_cache() -> None:
    # Hammer the cached loader a bunch of times to make sure the underlying
    # frame is not mutated by filter_people().
    for _ in range(500):
        _ = filter_people(min_age=18, max_age=65)
        time.sleep(0.01)
    assert len(load_people()) == 100
