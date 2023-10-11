from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.users import Users, UserCreate
from utils import utils

users_router = APIRouter()

# async ?
@users_router.get("/")
async def get_user_by_userid(user_id: int, db: Session = Depends(utils.get_db)):
    return db.query(Users).filter(Users.id == user_id).first()


@users_router.post("/")
async def register_user(user_details: UserCreate, db: Session = Depends(utils.get_db)):
    try:
        new_user = Users(
            name=user_details.name,
            email=user_details.email,
            contact_num=user_details.contact_num,
            kotak_username=user_details.kotak_username,
            supervisor_id=user_details.supervisor_id,
            organization_id=user_details.organization_id,
        )
        db.add(new_user)
        db.commit()
        return {"status": "SUCCESS"}
    except Exception as e:
        return {"status": "FAILURE", "message": str(e)}
