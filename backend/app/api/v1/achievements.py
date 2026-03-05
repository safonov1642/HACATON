from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.models import User, Achievement, UserAchievement
from app.schemas.achievement import AchievementOut, UserAchievementOut, UpdateProgressRequest
from app.services.achievement_service import update_achievement_progress

router = APIRouter(prefix="/achievements", tags=["Achievements"])

@router.get("/", response_model=list[AchievementOut])
def get_all_achievements(db: Session = Depends(get_db)):
    """Получить список всех достижений (справочник)."""
    achievements = db.query(Achievement).all()
    return achievements

@router.get("/my", response_model=list[UserAchievementOut])
def get_my_achievements(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Получить прогресс текущего пользователя по всем достижениям."""
    progress = db.query(UserAchievement).filter(UserAchievement.user_id == current_user.id).all()
    return progress

@router.post("/progress")
def update_progress(
    request: UpdateProgressRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить прогресс по достижению (например, добавить 1 час)."""
    result = update_achievement_progress(db, current_user, request.achievement_type, request.increment)
    if result is None:
        raise HTTPException(404, "Achievement type not found")
    return {"message": "Progress updated", "current_value": result.current_value}