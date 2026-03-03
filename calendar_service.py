from sqlalchemy.orm import Session
from datetime import datetime, date
from app.models import Booking, Zone, GlobalRestriction

def get_schedule(db: Session, target_date: date):
    """
    Возвращает для каждой зоны список активных броней на указанную дату,
    а также глобальные ограничения на эту дату.
    """
    start = datetime.combine(target_date, datetime.min.time())
    end = datetime.combine(target_date, datetime.max.time())

    bookings = db.query(Booking).filter(
        Booking.start_time >= start,
        Booking.start_time < end,
        Booking.status == "active"
    ).all()

    # Группируем по zone_id
    bookings_by_zone = {}
    for b in bookings:
        if b.zone_id not in bookings_by_zone:
            bookings_by_zone[b.zone_id] = []
        bookings_by_zone[b.zone_id].append({
            "start": b.start_time,
            "end": b.end_time,
            "user_name": b.user.full_name if not b.user.is_admin else "Admin"
        })

    zones = db.query(Zone).filter(Zone.is_active == True).all()
    result = []
    for zone in zones:
        result.append({
            "zone_id": zone.id,
            "zone_name": zone.name,
            "bookings": bookings_by_zone.get(zone.id, [])
        })

    # Глобальные ограничения на этот день
    day_of_week = target_date.weekday()
    restrictions = db.query(GlobalRestriction).filter(
        GlobalRestriction.day_of_week == day_of_week
    ).all()
    global_slots = []
    for r in restrictions:
        res_start = datetime.combine(target_date, r.start_time)
        res_end = datetime.combine(target_date, r.end_time)
        global_slots.append({
            "start": res_start,
            "end": res_end,
            "user_name": r.description or "Занято (пары)"
        })

    return result, global_slots