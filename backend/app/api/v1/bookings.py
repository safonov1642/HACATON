from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db, get_current_user, get_current_admin
from app.models import User, Booking, Zone
from app.schemas.booking import BookingCreate, BookingOut, BookingMarkNoShow
from app.services import booking_service
from datetime import datetime

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingOut)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Проверка блокировки
    if not booking_service.check_user_blocked(current_user):
        raise HTTPException(400, "You are blocked due to no-shows")

    zone = db.get(Zone, booking.zone_id)
    if not zone or not zone.is_active:
        raise HTTPException(404, "Zone not found")

    # Проверка глобальных ограничений
    if not booking_service.check_global_restrictions(db, booking.start_time, booking.end_time):
        raise HTTPException(400, "Booking is not allowed during class hours")

    # Проверка доступности слота
    if not booking_service.is_zone_available(db, booking.zone_id, booking.start_time, booking.end_time):
        raise HTTPException(400, "This time slot is already booked")

    new_booking = booking_service.create_booking(db, current_user.id, booking.zone_id, booking.start_time, booking.end_time)
    return new_booking

@router.get("/my", response_model=List[BookingOut])
def get_my_bookings(
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Booking).filter(Booking.user_id == current_user.id)
    if status:
        query = query.filter(Booking.status == status)
    return query.all()

@router.patch("/{booking_id}/cancel", response_model=BookingOut)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.get(Booking, booking_id)
    if not booking or booking.user_id != current_user.id:
        raise HTTPException(404, "Booking not found")
    cancelled = booking_service.cancel_booking(db, booking)
    if not cancelled:
        raise HTTPException(400, "Cannot cancel booking less than {} minutes before start".format(settings.CANCELLATION_WINDOW_MINUTES))
    return cancelled

# Админские эндпоинты
@router.get("/", response_model=List[BookingOut])
def get_all_bookings(
    user_id: int = None,
    zone_id: int = None,
    status: str = None,
    from_date: datetime = None,
    to_date: datetime = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    query = db.query(Booking)
    if user_id:
        query = query.filter(Booking.user_id == user_id)
    if zone_id:
        query = query.filter(Booking.zone_id == zone_id)
    if status:
        query = query.filter(Booking.status == status)
    if from_date:
        query = query.filter(Booking.start_time >= from_date)
    if to_date:
        query = query.filter(Booking.start_time <= to_date)
    return query.all()

@router.post("/{booking_id}/mark-no-show")
def mark_no_show(
    booking_id: int,
    data: BookingMarkNoShow,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.status != "active":
        raise HTTPException(400, "Only active bookings can be marked as no-show")
    booking.status = "no_show"
    db.commit()
    booking_service.apply_penalty(db, data.user_id)
    return {"message": "Booking marked as no-show, user penalized"}