"""Shared fixtures. Clears the in-memory audience store between tests."""
import pytest
from fastapi.testclient import TestClient

from app import main
from app.data import load_people


@pytest.fixture
def client() -> TestClient:
    main._audiences.clear()
    return TestClient(main.app)


@pytest.fixture(autouse=True, scope="session")
def _warm_cache() -> None:
    load_people()
