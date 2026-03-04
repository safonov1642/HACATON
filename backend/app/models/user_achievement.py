from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserAchievement(Base):
    __tablename__ = "user_achievements"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), primary_key=True)
    current_value = Column(Integer, default=0)
    completed_levels = Column(JSON, default=list)  # список достигнутых уровней, например ["bronze", "silver"]

    user = relationship("User")
    achievement = relationship("Achievement")