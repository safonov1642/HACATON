from pydantic import BaseModel
from typing import Optional
from datetime import time

class ZoneBase(BaseModel):
    name: str
    type: Optional[str] = None
    capacity: int = 1
    working_hours_start: Optional[time] = None
    working_hours_end: Optional[time] = None

class ZoneCreate(ZoneBase):
    pass

class ZoneUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    capacity: Optional[int] = None
    working_hours_start: Optional[time] = None
    working_hours_end: Optional[time] = None
    is_active: Optional[bool] = None

class ZoneOut(ZoneBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True