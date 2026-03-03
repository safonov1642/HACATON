from sqlalchemy import Column, Integer, String, Boolean, JSON
from app.core.database import Base

class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'gaming', 'training', 'team'
    capacity = Column(Integer, nullable=False, default=1)
    description = Column(String, nullable=True)
    equipment = Column(JSON, nullable=True)  # список ["PC", "PS5", ...]
    price_per_hour = Column(Integer, default=0)  # для экономики
    age_restriction = Column(Integer, nullable=True)
    working_hours = Column(JSON, nullable=True)  # {"mon-fri": "10:00-22:00", ...}
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class ZoneBase(BaseModel):
    name: str
    type: str  # 'gaming', 'training', 'team'
    capacity: int
    description: Optional[str] = None
    equipment: Optional[List[str]] = None
    price_per_hour: Optional[int] = 0
    age_restriction: Optional[int] = None
    working_hours: Optional[Dict] = None
    is_active: bool = True

class ZoneCreate(ZoneBase):
    pass

class ZoneUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    capacity: Optional[int] = None
    description: Optional[str] = None
    equipment: Optional[List[str]] = None
    price_per_hour: Optional[int] = None
    age_restriction: Optional[int] = None
    working_hours: Optional[Dict] = None
    is_active: Optional[bool] = None

class ZoneOut(ZoneBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True