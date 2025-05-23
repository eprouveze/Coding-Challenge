import pytest
from datetime import datetime, timedelta
from src.models import Event, EventCategory, Attendee, AttendanceStatus, User, UserRole
from src.auth import get_password_hash

@pytest.fixture
def test_event(db, organizer_user):
    event = Event(
        title="Test Event",
        description="Test Description",
        date=datetime.utcnow() + timedelta(days=7),
        location="Test Location",
        capacity=2,
        category=EventCategory.CONFERENCE,
        organizer_id=organizer_user.id
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def test_register_for_event(client, test_event, auth_headers):
    response = client.post(
        "/attendees/register",
        headers=auth_headers,
        json={"event_id": test_event.id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Registered for event successfully"
    assert data["status"] == AttendanceStatus.REGISTERED

def test_register_duplicate(client, test_event, auth_headers):
    client.post(
        "/attendees/register",
        headers=auth_headers,
        json={"event_id": test_event.id}
    )
    
    response = client.post(
        "/attendees/register",
        headers=auth_headers,
        json={"event_id": test_event.id}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Already registered for this event"

def test_waitlist_when_full(client, db, test_event, auth_headers):
    user2 = User(
        email="user2@example.com",
        username="user2",
        hashed_password=get_password_hash("password"),
        role=UserRole.ATTENDEE
    )
    user3 = User(
        email="user3@example.com",
        username="user3",
        hashed_password=get_password_hash("password"),
        role=UserRole.ATTENDEE
    )
    db.add(user2)
    db.add(user3)
    db.commit()
    
    client.post("/attendees/register", headers=auth_headers, json={"event_id": test_event.id})
    
    response2 = client.post(
        "/users/token",
        data={"username": "user2", "password": "password"}
    )
    headers2 = {"Authorization": f"Bearer {response2.json()['access_token']}"}
    client.post("/attendees/register", headers=headers2, json={"event_id": test_event.id})
    
    response3 = client.post(
        "/users/token",
        data={"username": "user3", "password": "password"}
    )
    headers3 = {"Authorization": f"Bearer {response3.json()['access_token']}"}
    response = client.post("/attendees/register", headers=headers3, json={"event_id": test_event.id})
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == AttendanceStatus.WAITLISTED
    assert data["waitlist_position"] == 1

def test_check_in_attendee(client, db, test_event, test_user, admin_headers):
    attendee = Attendee(
        event_id=test_event.id,
        user_id=test_user.id,
        status=AttendanceStatus.REGISTERED
    )
    db.add(attendee)
    db.commit()
    
    response = client.put(f"/attendees/{attendee.id}/check-in", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == AttendanceStatus.CHECKED_IN
    assert data["checked_in_at"] is not None

def test_cancel_registration(client, db, test_event, test_user, auth_headers):
    attendee = Attendee(
        event_id=test_event.id,
        user_id=test_user.id,
        status=AttendanceStatus.REGISTERED
    )
    db.add(attendee)
    db.commit()
    
    response = client.put(f"/attendees/{attendee.id}/cancel", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == AttendanceStatus.CANCELLED

def test_get_my_registrations(client, db, test_event, test_user, auth_headers):
    attendee = Attendee(
        event_id=test_event.id,
        user_id=test_user.id,
        status=AttendanceStatus.REGISTERED
    )
    db.add(attendee)
    db.commit()
    
    response = client.get("/attendees/my-registrations", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["event_id"] == test_event.id

def test_get_event_attendees(client, db, test_event, test_user, organizer_headers):
    attendee = Attendee(
        event_id=test_event.id,
        user_id=test_user.id,
        status=AttendanceStatus.REGISTERED
    )
    db.add(attendee)
    db.commit()
    
    response = client.get(f"/attendees/event/{test_event.id}", headers=organizer_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == test_user.id