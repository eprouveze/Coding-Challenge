from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "Event Management API"
    version: str = "1.0.0"
    database_url: str = "sqlite:///./event_management.db"
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    redis_url: Optional[str] = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"

settings = Settings()