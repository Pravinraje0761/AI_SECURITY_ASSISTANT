"""Run the API against a throwaway SQLite database."""
import os
import sys
import tempfile
from pathlib import Path

import pytest

_DB_DIR = tempfile.mkdtemp(prefix="bodyguard-test-")
os.environ["DATABASE_URL"] = f"sqlite:///{_DB_DIR}/test.db"
os.environ["SECRET_KEY"] = "test-only-secret"
os.environ["LOG_FILE"] = f"{_DB_DIR}/test.log"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def auth_headers(client):
    client.post("/api/v1/auth/register", json={
        "email": "tester@example.com", "password": "Test123!", "first_name": "Test", "last_name": "User"})
    r = client.post("/api/v1/auth/login", data={"username": "tester@example.com", "password": "Test123!"})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}
