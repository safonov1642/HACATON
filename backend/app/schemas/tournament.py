from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TournamentCreate(BaseModel):
    name: str
    game: str
    team_size: int
    date: datetime
    description: Optional[str] = None

class TournamentOut(BaseModel):
    id: int
    name: str
    game: str
    team_size: int
    date: datetime
    description: Optional[str] = None
    status: str
    created_by: int

    class Config:
        from_attributes = True

class TournamentDetail(TournamentOut):
    teams: List[dict]  # список зарегистрированных команд с рейтингом
    bracket: Optional[dict] = None