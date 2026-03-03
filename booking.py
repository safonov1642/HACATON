from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="active")  # active, cancelled, completed, no_show
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    cancelled_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User")
    zone = relationship("Zone")

    from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookingBase(BaseModel):
    zone_id: int
    start_time: datetime
    end_time: datetime

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    cancelled_at: Optional[datetime]

    class Config:
        from_attributes = True

class BookingCancel(BaseModel):
    pass  # можно добавить причину

class BookingMarkNoShow(BaseModel):
    user_id: int  # чью неявку отмечаем