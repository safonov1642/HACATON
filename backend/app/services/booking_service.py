from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Booking, Zone, Restriction, User
from app.core.config import settings

def is_zone_available(db: Session, zone_id: int, start: datetime, end: datetime) -> bool:
    """Проверить, свободна ли зона в заданный интервал."""
    existing = db.query(Booking).filter(
        Booking.zone_id == zone_id,
        Booking.status.in_(["active", "no_show"]),  # не учитываем отменённые и завершённые
        Booking.start_time < end,
        Booking.end_time > start
    ).first()
    return existing is None

def check_global_restrictions(db: Session, start: datetime, end: datetime) -> bool:
    """Проверить, нет ли глобальных ограничений (пар) в этот интервал."""
    restriction = db.query(Restriction).filter(
        Restriction.start_time < end,
        Restriction.end_time > start
    ).first()
    return restriction is None

def check_user_blocked(user: User) -> bool:
    """Проверить, не заблокирован ли пользователь."""
    if user.blocked_until and user.blocked_until > datetime.utcnow():
        return False
    return True

def create_booking(db: Session, user_id: int, zone_id: int, start: datetime, end: datetime) -> Booking:
    booking = Booking(
        user_id=user_id,
        zone_id=zone_id,
        start_time=start,
        end_time=end,
        status="active"
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def cancel_booking(db: Session, booking: Booking) -> Booking:
    """Отмена брони (доступно пользователю за N минут до начала)."""
    if booking.start_time - datetime.utcnow() < timedelta(minutes=settings.CANCELLATION_WINDOW_MINUTES):
        return None  # нельзя отменить
    booking.status = "cancelled"
    booking.cancelled_at = datetime.utcnow()
    db.commit()
    db.refresh(booking)
    return booking

def apply_penalty(db: Session, user_id: int):
    """Применить штраф за неявку: увеличить счётчик и, если превышен лимит, заблокировать."""
    # В реальности нужно хранить счётчик неявок. Для простоты создадим отдельную таблицу или поле в User.
    # Упрощённо: сразу блокируем пользователя на 24 часа при любой неявке.
    user = db.query(User).get(user_id)
    if user:
        user.blocked_until = datetime.utcnow() + timedelta(hours=settings.BLOCK_DURATION_HOURS)
        db.commit()