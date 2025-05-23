# Event Management System

A full-stack web application for managing events, tracking attendees, and providing analytics. Built with FastAPI (Python) backend and React (TypeScript) frontend.

## Features

### Core Features
- **Event Management**: Create, read, update, and delete events with categories
- **Attendee Management**: Register for events, automatic waitlist handling, check-in functionality
- **User Authentication**: JWT-based authentication with role-based access control
- **Analytics Dashboard**: Real-time statistics and data visualization
- **Real-time Updates**: WebSocket support for live notifications

### Advanced Features
- Role-based access control (Admin, Organizer, Attendee)
- Automatic waitlist processing when spots become available
- Responsive design with accessibility features
- Background task processing with Celery
- Comprehensive test coverage

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database interactions
- **SQLite** - Database (easily replaceable with PostgreSQL)
- **Celery** - Background task processing
- **Redis** - Message broker for Celery
- **JWT** - Authentication tokens

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Material-UI** - Component library
- **React Query** - Server state management
- **Zustand** - Client state management
- **Chart.js** - Data visualization
- **Vite** - Build tool

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Redis (for background tasks)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn src.main:app --reload
```

The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at http://localhost:3000

### Docker Setup

Run the entire application with Docker Compose:

```bash
docker-compose up --build
```

This will start:
- Backend API on http://localhost:8000
- Frontend on http://localhost:3000
- Redis for background tasks
- Celery worker

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /users/register` - Register new user
- `POST /users/token` - Login and get JWT token

#### Events
- `GET /events/` - List all events
- `POST /events/` - Create new event (Organizer/Admin)
- `PUT /events/{id}` - Update event (Organizer/Admin)
- `DELETE /events/{id}` - Delete event (Organizer/Admin)

#### Attendees
- `POST /attendees/register` - Register for event
- `PUT /attendees/{id}/check-in` - Check in attendee
- `PUT /attendees/{id}/cancel` - Cancel registration

#### Analytics
- `GET /analytics/events` - Event statistics
- `GET /analytics/users` - User statistics

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### End-to-End Tests
```bash
cd frontend
npm run e2e
```

## User Roles

1. **Admin**
   - Full access to all features
   - Can manage all events and users
   - Access to all analytics

2. **Organizer**
   - Can create and manage their own events
   - View attendees for their events
   - Access to event analytics

3. **Attendee**
   - Can browse and register for events
   - View their registrations
   - Basic user features

## Project Structure

```
event-management/
├── backend/
│   ├── src/
│   │   ├── routers/     # API endpoints
│   │   ├── models.py    # Database models
│   │   ├── schemas.py   # Pydantic schemas
│   │   ├── auth.py      # Authentication logic
│   │   └── main.py      # Application entry point
│   └── tests/           # Backend tests
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   ├── store/       # State management
│   │   └── types/       # TypeScript types
│   └── tests/           # Frontend tests
└── docker-compose.yml   # Docker configuration
```

## Deployment

### Environment Variables

Backend:
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret key
- `REDIS_URL` - Redis connection string

Frontend:
- `VITE_API_URL` - Backend API URL

### Production Considerations

1. Replace SQLite with PostgreSQL for production
2. Use environment-specific configuration
3. Enable HTTPS
4. Set up proper CORS configuration
5. Use a production-grade web server (Gunicorn/Nginx)
6. Implement rate limiting
7. Set up monitoring and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.