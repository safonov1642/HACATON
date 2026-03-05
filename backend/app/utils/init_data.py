from sqlalchemy.orm import Session
from app.models import Achievement, AchievementLevel

def init_achievements(db: Session):
    achievements_data = [
        {
            "title": "Часы в кибер арене",
            "description": "Проведите время за играми",
            "icon": "fa-solid fa-clock",
            "type": "hours",
            "levels": [
                {"level": "bronze", "target_value": 5, "rating": 10},
                {"level": "silver", "target_value": 20, "rating": 25},
                {"level": "gold", "target_value": 50, "rating": 50},
                {"level": "platinum", "target_value": 100, "rating": 100},
            ]
        },
        # ... остальные достижения
    ]

    for data in achievements_data:
        existing = db.query(Achievement).filter(Achievement.type == data["type"]).first()
        if not existing:
            ach = Achievement(
                title=data["title"],
                description=data["description"],
                icon=data["icon"],
                type=data["type"]
            )
            db.add(ach)
            db.flush()  # чтобы получить id
            for lvl in data["levels"]:
                level = AchievementLevel(
                    achievement_id=ach.id,
                    level=lvl["level"],
                    target_value=lvl["target_value"],
                    rating=lvl["rating"]
                )
                db.add(level)
    db.commit()