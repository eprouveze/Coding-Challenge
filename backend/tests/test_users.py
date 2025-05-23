import pytest
from src.models import UserRole

def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "password123",
            "full_name": "New User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert data["role"] == UserRole.ATTENDEE

def test_register_duplicate_email(client, test_user):
    response = client.post(
        "/users/register",
        json={
            "email": test_user.email,
            "username": "anotheruser",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_register_duplicate_username(client, test_user):
    response = client.post(
        "/users/register",
        json={
            "email": "another@example.com",
            "username": test_user.username,
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"

def test_login(client, test_user):
    response = client.post(
        "/users/token",
        data={"username": test_user.username, "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post(
        "/users/token",
        data={"username": "wronguser", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_get_current_user(client, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_update_current_user(client, auth_headers):
    response = client.put(
        "/users/me",
        headers=auth_headers,
        json={"full_name": "Updated Name"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"

def test_get_users_admin_only(client, auth_headers, admin_headers):
    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == 403
    
    response = client.get("/users/", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)