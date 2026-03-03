from sqlalchemy import Column, Integer, String, Time
from app.core.database import Base

class GlobalRestriction(Base):
    __tablename__ = "global_restrictions"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer, nullable=False)  # 0=пн, 1=вт, ... 6=вс (или можно хранить как строку)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    description = Column(String, nullable=True)  # например "пары"
    
    from pydantic import BaseModel
from datetime import time
from typing import Optional

class GlobalRestrictionBase(BaseModel):
    day_of_week: int  # 0-6
    start_time: time
    end_time: time
    description: Optional[str] = None

class GlobalRestrictionCreate(GlobalRestrictionBase):
    pass

class GlobalRestrictionOut(GlobalRestrictionBase):
    id: int

    class Config:
        from_attributes = True