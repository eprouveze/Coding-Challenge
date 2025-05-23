from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging

from src.core.config import settings
from src.core.database import engine, Base
from src.core.websocket import ConnectionManager
from src.api.routes import events, attendees, analytics, auth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Event Management API")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down Event Management API")

app = FastAPI(
    title="Event Management API",
    description="A comprehensive event management system built by Claude Sonnet 4",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
app.include_router(attendees.router, prefix="/api/v1/attendees", tags=["attendees"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Message received: {data}", client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id)

@app.get("/")
async def root():
    return {"message": "Event Management API by Claude Sonnet 4", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "event-management-api"}

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )