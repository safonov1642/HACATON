from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.core.database import get_db
from app.core.dependencies import get_current_admin

router = APIRouter(prefix="/zones", tags=["Zones"])

@router.get("/", response_model=List[schemas.ZoneOut])
def get_zones(
    type: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # любой авторизованный
):
    query = db.query(models.Zone).filter(models.Zone.is_active == True)
    if type:
        query = query.filter(models.Zone.type == type)
    return query.all()

@router.get("/{zone_id}", response_model=schemas.ZoneOut)
def get_zone(zone_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    zone = db.get(models.Zone, zone_id)
    if not zone or not zone.is_active:
        raise HTTPException(404, "Zone not found")
    return zone

@router.post("/", response_model=schemas.ZoneOut)
def create_zone(
    zone: schemas.ZoneCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    db_zone = models.Zone(**zone.dict())
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

@router.patch("/{zone_id}", response_model=schemas.ZoneOut)
def update_zone(
    zone_id: int,
    zone_update: schemas.ZoneUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    db_zone = db.get(models.Zone, zone_id)
    if not db_zone:
        raise HTTPException(404, "Zone not found")
    for key, value in zone_update.dict(exclude_unset=True).items():
        setattr(db_zone, key, value)
    db.commit()
    db.refresh(db_zone)
    return db_zone

@router.delete("/{zone_id}")
def delete_zone(
    zone_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    zone = db.get(models.Zone, zone_id)
    if not zone:
        raise HTTPException(404, "Zone not found")
    # мягкое удаление
    zone.is_active = False
    db.commit()
    return {"message": "Zone deactivated"}