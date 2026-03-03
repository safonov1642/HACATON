from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cyber Arena API"
    SECRET_KEY: str = "change_this_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./test.db"  # для разработки
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]  # для фронтенда
    CANCELLATION_WINDOW_MINUTES: int = 30  # за сколько минут можно отменить бронь
    MAX_NO_SHOWS: int = 3  # максимальное количество неявок до блокировки
    BLOCK_DURATION_HOURS: int = 24  # длительность блокировки

    class Config:
        env_file = ".env"

settings = Settings()