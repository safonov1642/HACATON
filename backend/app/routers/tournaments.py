# backend/app/routers/tournaments.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..database import get_db
from ..auth import get_current_user  # если нужна авторизация

router = APIRouter()

@router.post("/", response_model=schemas.Tournament)
def create_tournament(
    tournament: schemas.TournamentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # опционально
):
    """Создание нового турнира (только для авторизованных пользователей)."""
    return crud.create_tournament(db=db, tournament=tournament, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Tournament])
def read_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список турниров с пагинацией."""
    tournaments = crud.get_tournaments(db, skip=skip, limit=limit)
    return tournaments

@router.get("/{tournament_id}", response_model=schemas.Tournament)
def read_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """Получить информацию о конкретном турнире."""
    db_tournament = crud.get_tournament(db, tournament_id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return db_tournament

@router.post("/{tournament_id}/register", response_model=schemas.TournamentParticipant)
def register_for_tournament(
    tournament_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Зарегистрироваться на турнир."""
    return crud.register_user_for_tournament(db, user_id=current_user.id, tournament_id=tournament_id)