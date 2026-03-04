from pydantic import BaseModel
from typing import List

class AchievementLevelSchema(BaseModel):
    level: str
    target_value: int
    rating: int

class AchievementSchema(BaseModel):
    id: int
    title: str
    description: str
    icon: str
    type: str
    levels: List[AchievementLevelSchema]

    class Config:
        from_attributes = True

class UserAchievementSchema(BaseModel):
    user_id: int
    achievement_id: int
    current_value: int
    completed_levels: List[str]

    class Config:
        from_attributes = True