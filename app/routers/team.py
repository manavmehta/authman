from fastapi import APIRouter, Depends
from models.team import Team
from sqlalchemy.orm import Session

from db.connection import SessionLocal

team_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# async ?
@team_router.get("/")
async def get_team(team_id: int, db: Session = Depends(get_db)):
    return db.query(Team).filter(Team.id == team_id).first()
