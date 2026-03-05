from sqlalchemy import Column, Integer, String, Boolean, Time
from sqlalchemy.orm import relationship
from app.core.database import Base

class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String)  # например, "gaming", "training", "team"
    capacity = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    working_hours_start = Column(Time, nullable=True)  # опционально
    working_hours_end = Column(Time, nullable=True)

    bookings = relationship("Booking", back_populates="zone")