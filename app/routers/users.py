from fastapi import APIRouter, Depends
from models.users import Users
from sqlalchemy.orm import Session

from db.connection import SessionLocal

users_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# async ?
@users_router.get("/")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Users).filter(Users.id == user_id).first()
