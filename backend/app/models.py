# backend/app/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base
from datetime import datetime
from sqlalchemy.schema import ForeignKey

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    google_id = Column(String, unique=True, index=True) # ID от Google
    name = Column(String)
    avatar_url = Column(String, nullable=True)
    role = Column(String, default="student") # student, admin
    credits = Column(Integer, default=100) # Внутренняя валюта
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # backend/app/models.py
class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) # Например "Игровая зона A"
    type = Column(String) # "gaming", "training", "team"
    capacity = Column(Integer) # количество мест
    is_active = Column(Boolean, default=True)
    # Доп. поля: оборудование, стоимость в час (в credits), изображение
    class Booking(Base):
        __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    zone_id = Column(Integer, ForeignKey("zones.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="confirmed") # confirmed, cancelled, no-show
    created_at = Column(DateTime, default=datetime.utcnow)
    class Achievement(Base):
        __tablename__ = "achievements"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    icon = Column(String) # Название файла иконки или emoji
    condition_type = Column(String) # "bookings_count", "tournaments_won", "days_streak"
    condition_value = Column(Integer) # например 10 (бронирований)

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    progress = Column(Integer, default=0) # текущий прогресс (например, 5 из 10)
    achieved_at = Column(DateTime, nullable=True) # дата получения
    class ActivityFeed(Base):
        __tablename__ = "activity_feed"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    activity_type = Column(String) # "booking", "achievement", "tournament_start"
    message = Column(String) # "Иван забронировал игровую зону"
    related_link = Column(String, nullable=True) # ссылка на объект
    created_at = Column(DateTime, default=datetime.utcnow)