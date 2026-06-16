"""API tests for the audience builder."""
import time

import pytest
from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_audience_no_filters(client: TestClient) -> None:
    r = client.post(
        "/audiences",
        json={"name": "everyone", "filters": {}},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["id"] == 1
    assert body["name"] == "everyone"
    assert body["size"] == 100


def test_create_audience_with_age_range(client: TestClient) -> None:
    r = client.post(
        "/audiences",
        json={"name": "young adults", "filters": {"min_age": 18, "max_age": 30}},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["filters"] == {"min_age": 18, "max_age": 30}
    assert 0 <= body["size"] <= 100


def test_create_audience_rejects_inverted_range(client: TestClient) -> None:
    r = client.post(
        "/audiences",
        json={"name": "bad", "filters": {"min_age": 50, "max_age": 20}},
    )
    assert r.status_code == 422


def test_get_audience(client: TestClient) -> None:
    created = client.post(
        "/audiences",
        json={"name": "seniors", "filters": {"min_age": 65}},
    ).json()
    r = client.get(f"/audiences/{created['id']}")
    assert r.status_code == 200
    assert r.json()["name"] == "seniors"


def test_get_audience_not_found(client: TestClient) -> None:
    r = client.get("/audiences/9999")
    assert r.status_code == 404


def test_get_audience_members(client: TestClient) -> None:
    created = client.post(
        "/audiences",
        json={"name": "adults", "filters": {"min_age": 18}},
    ).json()
    r = client.get(f"/audiences/{created['id']}/members")
    assert r.status_code == 200
    members = r.json()["members"]
    assert len(members) == created["size"]
    for m in members:
        assert m["age"] >= 18
        assert set(m.keys()) == {
            "person_id",
            "age",
            "state",
            "first_name",
            "last_name",
        }


@pytest.mark.slow
def test_create_many_audiences_is_stable(client: TestClient) -> None:
    # Simulates a soak-style test that the CI should skip on PRs.
    for i in range(200):
        r = client.post(
            "/audiences",
            json={"name": f"a{i}", "filters": {"min_age": i % 80}},
        )
        assert r.status_code == 201
        time.sleep(0.02)


@pytest.mark.slow
def test_members_pagination_soak(client: TestClient) -> None:
    created = client.post(
        "/audiences",
        json={"name": "all", "filters": {}},
    ).json()
    for _ in range(150):
        r = client.get(f"/audiences/{created['id']}/members")
        assert r.status_code == 200
        time.sleep(0.02)
