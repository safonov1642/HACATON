from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    rating: int
    equipped_badge: Optional[str] = None
    equipped_background: Optional[str] = None
    is_admin: bool
    blocked_until: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    equipped_badge: Optional[str] = None
    equipped_background: Optional[str] = None