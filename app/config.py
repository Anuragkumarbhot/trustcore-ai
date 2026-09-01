from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "TRUSTCORE AI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./trustcore.db"
    ALLOWED_ORIGINS: List[str] = ["http://localhost", "http://127.0.0.1"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()