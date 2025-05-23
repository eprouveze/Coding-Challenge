# Setup Guide

## Development Environment Setup

### Prerequisites

1. **Python 3.11+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify: `python --version`

2. **Node.js 18+**
   - Download from [nodejs.org](https://nodejs.org/)
   - Verify: `node --version` and `npm --version`

3. **Git**
   - Download from [git-scm.com](https://git-scm.com/)
   - Verify: `git --version`

4. **Redis** (for background tasks)
   - macOS: `brew install redis`
   - Ubuntu: `sudo apt-get install redis-server`
   - Windows: Use WSL or Docker

5. **Docker** (optional, for containerized setup)
   - Download from [docker.com](https://www.docker.com/)

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/eprouveze/Coding-Challenge.git
cd Coding-Challenge
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "SECRET_KEY=your-secret-key-here" > .env
echo "DATABASE_URL=sqlite:///./event_management.db" >> .env
echo "REDIS_URL=redis://localhost:6379" >> .env

# Run database migrations (creates tables)
python -c "from src.database import engine; from src.models import Base; Base.metadata.create_all(bind=engine)"

# Start the backend server
uvicorn src.main:app --reload --port 8000
```

#### 3. Frontend Setup

In a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

#### 4. Start Redis and Celery

In another terminal:

```bash
# Start Redis
redis-server

# In yet another terminal, start Celery worker
cd backend
celery -A src.tasks worker --loglevel=info
```

### Docker Setup

For a simpler setup using Docker:

```bash
# From the project root
docker-compose up --build
```

This starts all services:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Redis: localhost:6379
- Celery worker

## Initial Data Setup

### Create Admin User

1. Register a new user through the UI
2. Update their role in the database:

```python
# Run in Python shell with virtual environment activated
from src.database import SessionLocal
from src.models import User, UserRole

db = SessionLocal()
user = db.query(User).filter(User.username == "admin").first()
user.role = UserRole.ADMIN
db.commit()
```

### Create Sample Data

```python
from datetime import datetime, timedelta
from src.models import Event, EventCategory

# Create sample events
events = [
    Event(
        title="Tech Conference 2024",
        description="Annual technology conference",
        date=datetime.now() + timedelta(days=30),
        location="Convention Center",
        capacity=500,
        category=EventCategory.CONFERENCE,
        organizer_id=user.id
    ),
    Event(
        title="Python Workshop",
        description="Learn advanced Python techniques",
        date=datetime.now() + timedelta(days=15),
        location="Tech Hub",
        capacity=50,
        category=EventCategory.WORKSHOP,
        organizer_id=user.id
    )
]

for event in events:
    db.add(event)
db.commit()
```

## Configuration

### Backend Configuration

Edit `backend/src/config.py` or use environment variables:

```python
# Development settings
DATABASE_URL = "sqlite:///./event_management.db"
SECRET_KEY = "development-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# Production settings (use environment variables)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/dbname")
SECRET_KEY = os.getenv("SECRET_KEY", "production-secret-key")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### Frontend Configuration

Edit `frontend/vite.config.ts` for API proxy settings:

```typescript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

## Testing

### Backend Tests
```bash
cd backend
pytest -v
pytest --cov=src --cov-report=html  # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:ui  # Interactive test UI
```

### End-to-End Tests
```bash
cd frontend
npm run e2e
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill the process
   kill -9 <PID>
   ```

2. **Database connection errors**
   - Ensure SQLite file has proper permissions
   - For PostgreSQL, check connection string
   - Verify database server is running

3. **Redis connection errors**
   - Check Redis is running: `redis-cli ping`
   - Verify Redis URL in configuration
   - Check firewall settings

4. **CORS errors**
   - Ensure backend CORS middleware is configured
   - Check frontend proxy settings
   - Verify API base URL

5. **Module import errors**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`
   - Check PYTHONPATH includes project root

### Development Tips

1. **Hot Reloading**
   - Backend: Use `--reload` flag with uvicorn
   - Frontend: Vite provides hot module replacement

2. **Database Management**
   - Use SQLite Browser for visual inspection
   - Alembic for migrations in production
   - Regular backups of development data

3. **API Testing**
   - Use Swagger UI at http://localhost:8000/docs
   - Postman or Insomnia for complex scenarios
   - curl for quick command-line testing

4. **Debugging**
   - Backend: Use Python debugger (`pdb`)
   - Frontend: React Developer Tools
   - Network tab for API debugging

## Production Deployment

### Environment Variables

Set these in your production environment:

```bash
# Backend
DATABASE_URL=postgresql://user:password@host/database
SECRET_KEY=strong-random-secret-key
REDIS_URL=redis://redis-host:6379
CORS_ORIGINS=https://your-frontend-domain.com

# Frontend
VITE_API_URL=https://api.your-domain.com
```

### Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use HTTPS in production
- [ ] Configure CORS properly
- [ ] Enable rate limiting
- [ ] Set up monitoring and logging
- [ ] Regular security updates
- [ ] Backup strategy in place