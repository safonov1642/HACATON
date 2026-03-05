from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user, get_current_admin
from app.models import Zone, User
from app.schemas.zone import ZoneCreate, ZoneUpdate, ZoneOut

router = APIRouter(prefix="/zones", tags=["Zones"])

@router.get("/", response_model=List[ZoneOut])
def get_zones(type: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Zone).filter(Zone.is_active == True)
    if type:
        query = query.filter(Zone.type == type)
    return query.all()

@router.get("/{zone_id}", response_model=ZoneOut)
def get_zone(zone_id: int, db: Session = Depends(get_db)):
    zone = db.get(Zone, zone_id)
    if not zone or not zone.is_active:
        raise HTTPException(404, "Zone not found")
    return zone

@router.post("/", response_model=ZoneOut)
def create_zone(zone: ZoneCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    db_zone = Zone(**zone.dict())
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

@router.patch("/{zone_id}", response_model=ZoneOut)
def update_zone(zone_id: int, zone_update: ZoneUpdate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    db_zone = db.get(Zone, zone_id)
    if not db_zone:
        raise HTTPException(404, "Zone not found")
    for key, value in zone_update.dict(exclude_unset=True).items():
        setattr(db_zone, key, value)
    db.commit()
    db.refresh(db_zone)
    return db_zone

@router.delete("/{zone_id}")
def delete_zone(zone_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    zone = db.get(Zone, zone_id)
    if not zone:
        raise HTTPException(404, "Zone not found")
    zone.is_active = False
    db.commit()
    return {"message": "Zone deactivated"}