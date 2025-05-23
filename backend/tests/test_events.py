from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import tempfile
import pytest
from fastapi.testclient import TestClient

from backend.src.main import app, get_db
from backend.src.db import Base, SessionLocal, engine

# use temp database for tests
TEST_DB = "sqlite:///./test_test.db"

# Override engine
engine_test = create_engine(TEST_DB, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine_test)
Base.metadata.create_all(bind=engine_test)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_and_get_event():
    response = client.post(
        "/events/",
        json={
            "title": "Test Event",
            "description": "A test event",
            "date": "2030-01-01T00:00:00",
            "location": "Test Location",
            "capacity": 100,
            "category": "test",
        },
    )
    assert response.status_code == 200
    data = response.json()
    event_id = data["id"]

    get_resp = client.get(f"/events/{event_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Test Event"
