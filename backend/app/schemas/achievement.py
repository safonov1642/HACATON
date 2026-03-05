from pydantic import BaseModel
from typing import List, Optional

class AchievementLevelBase(BaseModel):
    level: str
    target_value: int
    rating: int

class AchievementLevelCreate(AchievementLevelBase):
    pass

class AchievementLevelOut(AchievementLevelBase):
    id: int
    achievement_id: int

    class Config:
        from_attributes = True

class AchievementBase(BaseModel):
    title: str
    description: Optional[str] = None
    icon: str
    type: str

class AchievementCreate(AchievementBase):
    levels: List[AchievementLevelCreate]

class AchievementOut(AchievementBase):
    id: int
    levels: List[AchievementLevelOut]

    class Config:
        from_attributes = True

class UserAchievementBase(BaseModel):
    user_id: int
    achievement_id: int
    current_value: int
    completed_levels: List[str]

class UserAchievementOut(UserAchievementBase):
    class Config:
        from_attributes = True

class UpdateProgressRequest(BaseModel):
    achievement_type: str  # например, "hours"
    increment: int = 1