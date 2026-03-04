from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    icon = Column(String)  # класс иконки, например "fa-solid fa-clock"
    type = Column(String, unique=True, nullable=False)  # hours, solo_wins, team_wins, games_participated
    levels = relationship("AchievementLevel", back_populates="achievement", cascade="all, delete-orphan")

class AchievementLevel(Base):
    __tablename__ = "achievement_levels"

    id = Column(Integer, primary_key=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    level = Column(String)  # bronze, silver, gold, platinum
    target_value = Column(Integer)
    rating = Column(Integer)

    achievement = relationship("Achievement", back_populates="levels")