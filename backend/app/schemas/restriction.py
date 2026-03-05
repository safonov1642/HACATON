from pydantic import BaseModel
from datetime import datetime

class RestrictionBase(BaseModel):
    name: str
    start_time: datetime
    end_time: datetime
    is_recurring: bool = False

class RestrictionCreate(RestrictionBase):
    pass

class RestrictionOut(RestrictionBase):
    id: int

    class Config:
        from_attributes = True