# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <token>
```

### Register User
```http
POST /users/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

### Login
```http
POST /users/token
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=securepassword
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Events

### List Events
```http
GET /events/?category=conference&upcoming_only=true&skip=0&limit=10
```

Query Parameters:
- `category` (optional): Filter by event category
- `upcoming_only` (optional, default: true): Show only future events
- `skip` (optional, default: 0): Pagination offset
- `limit` (optional, default: 100): Page size

### Get Event Details
```http
GET /events/{event_id}
```

### Create Event (Organizer/Admin)
```http
POST /events/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Tech Conference 2024",
  "description": "Annual technology conference",
  "date": "2024-06-15T10:00:00",
  "location": "Convention Center, New York",
  "capacity": 500,
  "category": "conference"
}
```

### Update Event (Organizer/Admin)
```http
PUT /events/{event_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Title",
  "capacity": 600
}
```

### Delete Event (Organizer/Admin)
```http
DELETE /events/{event_id}
Authorization: Bearer <token>
```

## Attendees

### Register for Event
```http
POST /attendees/register
Authorization: Bearer <token>
Content-Type: application/json

{
  "event_id": 1
}
```

Response:
```json
{
  "message": "Registered for event successfully",
  "status": "registered",
  "waitlist_position": null
}
```

### Check-in Attendee (Organizer/Admin)
```http
PUT /attendees/{attendee_id}/check-in
Authorization: Bearer <token>
```

### Cancel Registration
```http
PUT /attendees/{attendee_id}/cancel
Authorization: Bearer <token>
```

### Get My Registrations
```http
GET /attendees/my-registrations
Authorization: Bearer <token>
```

### Get Event Attendees (Organizer/Admin)
```http
GET /attendees/event/{event_id}
Authorization: Bearer <token>
```

## Analytics

### Event Statistics (Admin/Organizer)
```http
GET /analytics/events
Authorization: Bearer <token>
```

Response:
```json
{
  "total_events": 25,
  "total_attendees": 1500,
  "average_attendance_rate": 75.5,
  "events_by_category": {
    "conference": 10,
    "workshop": 8,
    "seminar": 7
  },
  "upcoming_events": 15,
  "past_events": 10,
  "most_popular_category": "conference",
  "events_at_capacity": 5
}
```

### User Statistics (Admin)
```http
GET /analytics/users
Authorization: Bearer <token>
```

### Event-Specific Statistics (Admin/Organizer)
```http
GET /analytics/events/{event_id}/stats
Authorization: Bearer <token>
```

## Users

### Get Current User
```http
GET /users/me
Authorization: Bearer <token>
```

### Update Current User
```http
PUT /users/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "full_name": "John Smith",
  "email": "johnsmith@example.com"
}
```

### List All Users (Admin)
```http
GET /users/?skip=0&limit=100
Authorization: Bearer <token>
```

### Update User (Admin)
```http
PUT /users/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "role": "organizer"
}
```

## WebSocket

### Real-time Updates
```
ws://localhost:8000/ws
```

Connect to receive real-time updates about:
- Event changes
- Registration updates
- Waitlist notifications

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Event not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "capacity"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- Anonymous users: 60 requests per hour
- Authenticated users: 600 requests per hour
- Admin users: Unlimited

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 600
X-RateLimit-Remaining: 599
X-RateLimit-Reset: 1640995200
```