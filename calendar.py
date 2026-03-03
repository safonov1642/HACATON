from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Slot(BaseModel):
    start: datetime
    end: datetime
    user_name: Optional[str] = None  # можно скрыть для приватности

class ZoneSchedule(BaseModel):
    zone_id: int
    zone_name: str
    bookings: List[Slot]

class CalendarResponse(BaseModel):
    zones: List[ZoneSchedule]
    global_restrictions: List[Slot]  # запрещённые интервалы (пары)

    from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.services import calendar_service
from app.schemas.calendar import CalendarResponse, ZoneSchedule, Slot

router = APIRouter(prefix="/calendar", tags=["Calendar"])

@router.get("/schedule", response_model=CalendarResponse)
def get_schedule(
    date: date = Query(..., description="Date in YYYY-MM-DD"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # любой авторизованный
):
    zone_slots, global_slots = calendar_service.get_schedule(db, date)

    # Преобразуем в формат Pydantic
    zones = []
    for z in zone_slots:
        bookings = [Slot(start=b["start"], end=b["end"], user_name=b["user_name"]) for b in z["bookings"]]
        zones.append(ZoneSchedule(zone_id=z["zone_id"], zone_name=z["zone_name"], bookings=bookings))

    restrictions = [Slot(start=r["start"], end=r["end"], user_name=r["user_name"]) for r in global_slots]

    return CalendarResponse(zones=zones, global_restrictions=restrictions)