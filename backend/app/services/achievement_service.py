from sqlalchemy.orm import Session
from app.models import Achievement, UserAchievement, User
from app.schemas.achievement import UpdateProgressRequest
import json

def update_achievement_progress(db: Session, user: User, achievement_type: str, increment: int = 1):
    # Найти достижение по типу
    achievement = db.query(Achievement).filter(Achievement.type == achievement_type).first()
    if not achievement:
        return None  # или raise exception

    # Получить или создать запись прогресса пользователя
    user_ach = db.query(UserAchievement).filter_by(
        user_id=user.id, achievement_id=achievement.id
    ).first()
    if not user_ach:
        user_ach = UserAchievement(
            user_id=user.id,
            achievement_id=achievement.id,
            current_value=0,
            completed_levels=[]
        )
        db.add(user_ach)
        db.flush()  # чтобы получить id, но не коммитить

    # Увеличить текущее значение
    user_ach.current_value += increment

    # Получить все уровни достижения, отсортированные по целевому значению
    levels = sorted(achievement.levels, key=lambda lvl: lvl.target_value)

    # Определить, какие уровни достигнуты (те, у которых target <= current_value)
    newly_completed = []
    for lvl in levels:
        if lvl.target_value <= user_ach.current_value and lvl.level not in user_ach.completed_levels:
            newly_completed.append(lvl.level)
            user_ach.completed_levels.append(lvl.level)

    # Если есть новые завершённые уровни, пересчитать рейтинг пользователя
    if newly_completed:
        # Получить все записи прогресса пользователя
        all_progress = db.query(UserAchievement).filter(UserAchievement.user_id == user.id).all()
        total_rating = 0
        for prog in all_progress:
            # Для каждого достижения получить уровни
            ach = prog.achievement
            for lvl in ach.levels:
                if lvl.level in prog.completed_levels:
                    total_rating += lvl.rating
        user.rating = total_rating

    db.commit()
    db.refresh(user_ach)
    return user_ach