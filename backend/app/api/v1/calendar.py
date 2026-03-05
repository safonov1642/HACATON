from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime, time
from app.core.dependencies import get_db, get_current_user
from app.models import Zone, Booking, Restriction
from typing import List

router = APIRouter(prefix="/calendar", tags=["Calendar"])

@router.get("/schedule")
def get_schedule(target_date: date, db: Session = Depends(get_db)):
    # Получить все активные зоны
    zones = db.query(Zone).filter(Zone.is_active == True).all()
    # Определить начало и конец дня
    start_of_day = datetime.combine(target_date, time.min)
    end_of_day = datetime.combine(target_date, time.max)

    # Получить все брони на этот день
    bookings = db.query(Booking).filter(
        Booking.start_time >= start_of_day,
        Booking.end_time <= end_of_day,
        Booking.status.in_(["active", "no_show"])
    ).all()

    # Получить глобальные ограничения на этот день
    restrictions = db.query(Restriction).filter(
        Restriction.start_time >= start_of_day,
        Restriction.end_time <= end_of_day
    ).all()

    # Сгруппировать брони по зонам
    result = []
    for zone in zones:
        zone_bookings = [b for b in bookings if b.zone_id == zone.id]
        result.append({
            "zone_id": zone.id,
            "zone_name": zone.name,
            "bookings": [
                {
                    "start": b.start_time.isoformat(),
                    "end": b.end_time.isoformat(),
                    "user_name": b.user.full_name
                } for b in zone_bookings
            ]
        })

    return {
        "date": target_date.isoformat(),
        "zones": result,
        "global_restrictions": [
            {"start": r.start_time.isoformat(), "end": r.end_time.isoformat(), "name": r.name}
            for r in restrictions
        ]
    }