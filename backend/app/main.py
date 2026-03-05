# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, tournaments, bookings, zones, achievements, teams, feed, admin
from .database import engine, Base

# Создание таблиц в БД (для простоты можно оставить здесь, лучше использовать Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CyberArena API", version="1.0.0")

# Настройка CORS – разрешаем запросы с любого источника (для разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tournaments.router, prefix="/api/tournaments", tags=["Tournaments"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(zones.router, prefix="/api/zones", tags=["Zones"])
app.include_router(achievements.router, prefix="/api/achievements", tags=["Achievements"])
app.include_router(teams.router, prefix="/api/teams", tags=["Teams"])
app.include_router(feed.router, prefix="/api/feed", tags=["Feed"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
def root():
    return {"message": "CyberArena API is running"}