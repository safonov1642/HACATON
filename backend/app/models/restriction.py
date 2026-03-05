from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.core.database import Base

class Restriction(Base):
    __tablename__ = "restrictions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # например, "Пары"
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_recurring = Column(Boolean, default=False)  # повторяется каждую неделю? можно усложнить
    # для простоты пока без сложных правил повторения