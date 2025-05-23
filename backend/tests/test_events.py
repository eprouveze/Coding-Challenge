import pytest
from datetime import datetime, timedelta
from src.models import EventCategory, Event

def test_create_event(client, organizer_headers):
    event_data = {
        "title": "Test Conference",
        "description": "A test event",
        "date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        "location": "Test Location",
        "capacity": 100,
        "category": EventCategory.CONFERENCE
    }
    response = client.post("/events/", headers=organizer_headers, json=event_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Conference"
    assert data["capacity"] == 100
    assert data["current_attendees"] == 0
    assert data["available_spots"] == 100

def test_create_event_unauthorized(client, auth_headers):
    event_data = {
        "title": "Test Conference",
        "description": "A test event",
        "date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        "location": "Test Location",
        "capacity": 100,
        "category": EventCategory.CONFERENCE
    }
    response = client.post("/events/", headers=auth_headers, json=event_data)
    assert response.status_code == 403

def test_get_events(client, db, organizer_user):
    for i in range(5):
        event = Event(
            title=f"Event {i}",
            description=f"Description {i}",
            date=datetime.utcnow() + timedelta(days=i+1),  # Ensure all are in future
            location=f"Location {i}",
            capacity=50,
            category=EventCategory.WORKSHOP,
            organizer_id=organizer_user.id
        )
        db.add(event)
    db.commit()
    
    response = client.get("/events/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5  # May include events from other tests

def test_get_events_with_filters(client, db, organizer_user):
    event1 = Event(
        title="Conference Event",
        date=datetime.utcnow() + timedelta(days=1),
        location="Location 1",
        capacity=100,
        category=EventCategory.CONFERENCE,
        organizer_id=organizer_user.id
    )
    event2 = Event(
        title="Workshop Event",
        date=datetime.utcnow() + timedelta(days=2),
        location="Location 2",
        capacity=50,
        category=EventCategory.WORKSHOP,
        organizer_id=organizer_user.id
    )
    db.add(event1)
    db.add(event2)
    db.commit()
    
    response = client.get("/events/?category=conference")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Conference Event"

def test_get_event_by_id(client, db, organizer_user):
    event = Event(
        title="Test Event",
        date=datetime.utcnow() + timedelta(days=1),
        location="Test Location",
        capacity=100,
        category=EventCategory.SEMINAR,
        organizer_id=organizer_user.id
    )
    db.add(event)
    db.commit()
    
    response = client.get(f"/events/{event.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Event"
    assert "attendees" in data

def test_update_event(client, db, organizer_user, organizer_headers):
    event = Event(
        title="Original Title",
        date=datetime.utcnow() + timedelta(days=1),
        location="Original Location",
        capacity=100,
        category=EventCategory.NETWORKING,
        organizer_id=organizer_user.id
    )
    db.add(event)
    db.commit()
    
    update_data = {"title": "Updated Title", "capacity": 150}
    response = client.put(f"/events/{event.id}", headers=organizer_headers, json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["capacity"] == 150

def test_delete_event(client, db, organizer_user, organizer_headers):
    event = Event(
        title="Event to Delete",
        date=datetime.utcnow() + timedelta(days=1),
        location="Location",
        capacity=50,
        category=EventCategory.SOCIAL,
        organizer_id=organizer_user.id
    )
    db.add(event)
    db.commit()
    
    response = client.delete(f"/events/{event.id}", headers=organizer_headers)
    assert response.status_code == 204
    
    response = client.get(f"/events/{event.id}")
    assert response.status_code == 404