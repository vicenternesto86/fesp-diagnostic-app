"""
FESP Diagnostic App - Configuration
"""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "FESP Diagnostic API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database - Supabase PostgreSQL or local SQLite
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./fesp_diagnostic.db"
    )
    
    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 
        "fesp-diagnostic-secret-key-change-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 hours
    
    # CORS - Allow frontend URLs
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        os.getenv("FRONTEND_URL", ""),
    ]
    
    # Traffic Light Thresholds
    RED_MAX: float = 1.9
    YELLOW_MAX: float = 3.4
    GREEN_MIN: float = 3.5
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

