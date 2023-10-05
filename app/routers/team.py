from fastapi import APIRouter, Depends
from models.team import Team
from sqlalchemy.orm import Session
from utils import utils

team_router = APIRouter()

# async ?
@team_router.get("/")
async def get_team(team_id: int, db: Session = Depends(utils.get_db)):
    return db.query(Team).filter(Team.id == team_id).first()
