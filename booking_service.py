from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Booking, Zone, GlobalRestriction, User
from app.schemas.booking import BookingCreate
from app.core.config import settings

def is_zone_available(db: Session, zone_id: int, start: datetime, end: datetime) -> bool:
    """
    Проверяет, свободен ли слот для бронирования (нет пересечений с active бронями)
    """
    overlapping = db.query(Booking).filter(
        Booking.zone_id == zone_id,
        Booking.status == "active",
        Booking.start_time < end,
        Booking.end_time > start
    ).first()
    return overlapping is None

def check_working_hours(zone: Zone, start: datetime, end: datetime) -> bool:
    """
    Проверяет, входит ли интервал в рабочие часы зоны.
    Если working_hours не заданы, считаем круглосуточно.
    """
    if not zone.working_hours:
        return True
    # Здесь нужна логика парсинга working_hours и проверки, что интервал целиком внутри.
    # Для упрощения будем считать, что зона работает всегда, если не задано.
    # В реальном проекте нужно реализовать проверку.
    return True

def check_global_restrictions(db: Session, start: datetime, end: datetime) -> bool:
    """
    Проверяет, не пересекается ли интервал с глобальными запретами (пары)
    """
    # Получаем день недели (0=пн, 6=вс) – зависит от локальных настроек
    day = start.weekday()  # для России понедельник=0
    restrictions = db.query(GlobalRestriction).filter(
        GlobalRestriction.day_of_week == day
    ).all()
    for r in restrictions:
        # Создаем datetime для начала и окончания ограничения в этот день
        res_start = datetime.combine(start.date(), r.start_time)
        res_end = datetime.combine(start.date(), r.end_time)
        # Если интервал пересекается с ограничением
        if start < res_end and end > res_start:
            return False
    return True

def check_user_blocked(user: User) -> bool:
    """
    Проверяет, не заблокирован ли пользователь
    """
    if user.blocked_until and user.blocked_until > datetime.utcnow():
        return False
    return True

def apply_penalty(db: Session, user_id: int):
    """
    Применяет наказание за неявку: блокирует пользователя на N часов/дней
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        # Например, блокировка на 24 часа
        user.blocked_until = datetime.utcnow() + timedelta(hours=24)
        db.commit()

def can_cancel_booking(booking: Booking) -> bool:
    """
    Проверяет, можно ли отменить бронь (например, не позже чем за 30 минут до начала)
    """
    if booking.status != "active":
        return False
    # Время до начала в минутах
    minutes_before = (booking.start_time - datetime.utcnow()).total_seconds() / 60
    return minutes_before >= settings.CANCELLATION_WINDOW_MINUTESs