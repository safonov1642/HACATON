from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    game = Column(String)
    team_size = Column(Integer)
    date = Column(DateTime)
    description = Column(String, nullable=True)
    status = Column(String, default="planned")  # planned, active, finished
    bracket = Column(JSON, nullable=True)       # упрощённая сетка
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    creator = relationship("User", foreign_keys=[created_by])
    registrations = relationship("TournamentRegistration", back_populates="tournament")

class TournamentRegistration(Base):
    __tablename__ = "tournament_registrations"

    tournament_id = Column(Integer, ForeignKey("tournaments.id"), primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), primary_key=True)
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)

    tournament = relationship("Tournament", back_populates="registrations")
    team = relationship("Team")