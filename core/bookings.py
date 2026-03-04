from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app import models, schemas
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_admin
from app.services import booking_service

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=schemas.BookingOut)
def create_booking(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Проверка блокировки пользователя
    if not booking_service.check_user_blocked(current_user):
        raise HTTPException(400, "You are blocked due to no-shows until {}".format(current_user.blocked_until))

    # Получить зону
    zone = db.get(models.Zone, booking.zone_id)
    if not zone or not zone.is_active:
        raise HTTPException(404, "Zone not found")

    # Проверка рабочего времени зоны
    if not booking_service.check_working_hours(zone, booking.start_time, booking.end_time):
        raise HTTPException(400, "Selected time is outside zone working hours")

    # Проверка глобальных ограничений (пары)
    if not booking_service.check_global_restrictions(db, booking.start_time, booking.end_time):
        raise HTTPException(400, "Booking is not allowed during class hours (pair)")

    # Проверка доступности слота
    if not booking_service.is_zone_available(db, booking.zone_id, booking.start_time, booking.end_time):
        raise HTTPException(400, "This time slot is already booked")

    # Создание брони
    db_booking = models.Booking(
        user_id=current_user.id,
        zone_id=booking.zone_id,
        start_time=booking.start_time,
        end_time=booking.end_time,
        status="active"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/my", response_model=List[schemas.BookingOut])
def get_my_bookings(
    status: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Booking).filter(models.Booking.user_id == current_user.id)
    if status:
        query = query.filter(models.Booking.status == status)
    return query.all()

@router.patch("/{booking_id}/cancel", response_model=schemas.BookingOut)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    booking = db.get(models.Booking, booking_id)
    if not booking or booking.user_id != current_user.id:
        raise HTTPException(404, "Booking not found")

    if not booking_service.can_cancel_booking(booking):
        raise HTTPException(400, "Cannot cancel booking less than {} minutes before start".format(
            settings.CANCELLATION_WINDOW_MINUTES))

    booking.status = "cancelled"
    booking.cancelled_at = datetime.utcnow()
    db.commit()
    db.refresh(booking)
    return booking

# Админские эндпоинты для бронирований
@router.get("/", response_model=List[schemas.BookingOut])
def get_all_bookings(
    user_id: int = None,
    zone_id: int = None,
    status: str = None,
    from_date: datetime = None,
    to_date: datetime = None,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    query = db.query(models.Booking)
    if user_id:
        query = query.filter(models.Booking.user_id == user_id)
    if zone_id:
        query = query.filter(models.Booking.zone_id == zone_id)
    if status:
        query = query.filter(models.Booking.status == status)
    if from_date:
        query = query.filter(models.Booking.start_time >= from_date)
    if to_date:
        query = query.filter(models.Booking.start_time <= to_date)
    return query.all()

@router.post("/{booking_id}/mark-no-show")
def mark_no_show(
    booking_id: int,
    data: schemas.BookingMarkNoShow,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    booking = db.get(models.Booking, booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    # Может быть только активная или завершённая? Лучше завершённую не менять.
    if booking.status != "active":
        raise HTTPException(400, "Only active bookings can be marked as no-show")

    booking.status = "no_show"
    db.commit()

    # Применить наказание к пользователю
    booking_service.apply_penalty(db, booking.user_id)

    return {"message": "Booking marked as no-show, user penalized"}