from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.core.database import get_db
from app.core.dependencies import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

# Управление глобальными ограничениями (пары)
@router.get("/restrictions", response_model=List[schemas.GlobalRestrictionOut])
def get_restrictions(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return db.query(models.GlobalRestriction).all()

@router.post("/restrictions", response_model=schemas.GlobalRestrictionOut)
def create_restriction(
    restriction: schemas.GlobalRestrictionCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_restriction = models.GlobalRestriction(**restriction.dict())
    db.add(db_restriction)
    db.commit()
    db.refresh(db_restriction)
    return db_restriction

@router.delete("/restrictions/{restriction_id}")
def delete_restriction(
    restriction_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    restriction = db.get(models.GlobalRestriction, restriction_id)
    if not restriction:
        raise HTTPException(404, "Restriction not found")
    db.delete(restriction)
    db.commit()
    return {"message": "Restriction deleted"}

# Управление пользователями (блокировка/разблокировка)
@router.post("/users/{user_id}/block")
def block_user(
    user_id: int,
    block_until: datetime,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    user.blocked_until = block_until
    db.commit()
    return {"message": f"User blocked until {block_until}"}

@router.post("/users/{user_id}/unblock")
def unblock_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    user.blocked_until = None
    db.commit()
    return {"message": "User unblocked"}