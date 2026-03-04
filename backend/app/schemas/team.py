from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TeamMemberSchema(BaseModel):
    user_id: int
    name: str  # full_name пользователя
    role: str
    rating: int

class TeamCreate(BaseModel):
    name: str
    game: str

class TeamOut(BaseModel):
    id: int
    name: str
    game: str
    average_rating: int
    captain_id: int
    members: List[TeamMemberSchema]
    tournaments_won: List[str]  # можно добавить позже

    class Config:
        from_attributes = True