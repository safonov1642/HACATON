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
    cancelled_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BookingCancel(BaseModel):
    pass  # можно добавить причину

class BookingMarkNoShow(BaseModel):
    user_id: int  # для админа