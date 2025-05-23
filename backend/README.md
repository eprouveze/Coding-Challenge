# Backend

A FastAPI application providing simple event management endpoints.

## Development

Create a virtual environment and install requirements from `requirements.txt`.
The tests rely on `httpx`, which is included in the requirements file.

Run the application:

```bash
uvicorn backend.src.main:app --reload
```

Run tests with pytest:

```bash
pytest
```
