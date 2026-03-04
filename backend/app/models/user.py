from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.core.database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    rating = Column(Integer, default=0)
    equipped_badge = Column(String, nullable=True)       # идентификатор значка
    equipped_background = Column(String, nullable=True) # CSS-градиент или путь
    is_admin = Column(Boolean, default=False)
    blocked_until = Column(DateTime, nullable=True)     # блокировка за неявки
    created_at = Column(DateTime, default=datetime.datetime.utcnow)