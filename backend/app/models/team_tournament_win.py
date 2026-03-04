from sqlalchemy import Column, Integer, ForeignKey, DateTime
from app.core.database import Base
import datetime

class TeamTournamentWin(Base):
    __tablename__ = "team_tournament_wins"

    team_id = Column(Integer, ForeignKey("teams.id"), primary_key=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), primary_key=True)
    won_at = Column(DateTime, default=datetime.datetime.utcnow)