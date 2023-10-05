from fastapi import APIRouter, Depends
from models.users import Users
from sqlalchemy.orm import Session
from utils import utils

users_router = APIRouter()

# async ?
@users_router.get("/")
async def get_user(user_id: int, db: Session = Depends(utils.get_db)):
    return db.query(Users).filter(Users.id == user_id).first()
