from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
from pathlib import Path
import tempfile
import pytest
import httpx
import asyncio
from httpx import ASGITransport

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

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

transport = ASGITransport(app=app)


def test_create_and_get_event():
    async def run():
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
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

            get_resp = await client.get(f"/events/{event_id}")
            assert get_resp.status_code == 200
            assert get_resp.json()["title"] == "Test Event"

    asyncio.run(run())
