import pytest
from datetime import datetime, timedelta
from src.models import Event, EventCategory, Attendee, AttendanceStatus, User, UserRole

def test_event_statistics(client, db, organizer_user, admin_headers):
    for i in range(3):
        event = Event(
            title=f"Event {i}",
            date=datetime.utcnow() + timedelta(days=i+1),  # Ensure all are in future
            location=f"Location {i}",
            capacity=100,
            category=EventCategory.CONFERENCE if i % 2 == 0 else EventCategory.WORKSHOP,
            organizer_id=organizer_user.id
        )
        db.add(event)
    db.commit()
    
    response = client.get("/analytics/events", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_events"] >= 3  # May include events from other tests
    assert data["upcoming_events"] >= 3
    assert "events_by_category" in data
    assert data["events_by_category"]["conference"] >= 2
    assert data["events_by_category"]["workshop"] >= 1

def test_user_statistics(client, db, admin_headers):
    for i in range(5):
        user = User(
            email=f"user{i}@example.com",
            username=f"user{i}",
            hashed_password="hashed",
            role=UserRole.ATTENDEE if i < 3 else UserRole.ORGANIZER,
            created_at=datetime.utcnow() - timedelta(days=i*10)
        )
        db.add(user)
    db.commit()
    
    response = client.get("/analytics/users", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_users"] >= 5
    assert "attendee" in data["users_by_role"]
    assert "organizer" in data["users_by_role"]
    assert data["users_by_role"]["attendee"] >= 3
    assert data["users_by_role"]["organizer"] >= 2

def test_event_specific_statistics(client, db, organizer_user, organizer_headers):
    event = Event(
        title="Test Event",
        date=datetime.utcnow() + timedelta(days=1),
        location="Test Location",
        capacity=10,
        category=EventCategory.SEMINAR,
        organizer_id=organizer_user.id
    )
    db.add(event)
    db.commit()
    
    for i in range(8):
        user = User(
            email=f"attendee{i}@example.com",
            username=f"attendee{i}",
            hashed_password="hashed",
            role=UserRole.ATTENDEE
        )
        db.add(user)
        db.flush()
        
        attendee = Attendee(
            event_id=event.id,
            user_id=user.id,
            status=AttendanceStatus.REGISTERED if i < 6 else AttendanceStatus.WAITLISTED
        )
        db.add(attendee)
    db.commit()
    
    response = client.get(f"/analytics/events/{event.id}/stats", headers=organizer_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["capacity"] == 10
    assert data["total_confirmed"] == 6
    assert data["attendance_rate"] == 60.0
    assert data["available_spots"] == 4
    assert not data["is_full"]