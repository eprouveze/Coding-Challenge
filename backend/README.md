# Event Management Backend

FastAPI-based REST API for event management with user authentication, event CRUD operations, attendee management with waitlist functionality, and analytics.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn src.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests with:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=src --cov-report=html
```

## Environment Variables

Create a `.env` file with:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./event_management.db
REDIS_URL=redis://localhost:6379
```

## Background Tasks

Celery is used for background tasks. Run worker with:
```bash
celery -A src.tasks worker --loglevel=info
```