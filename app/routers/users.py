from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.users import Users
from models.keycloak import KCUser
from utils import utils
from utils import keycloak_utils

users_router = APIRouter()


# async ?
@users_router.get("/")
async def get_allusers(db: Session = Depends(utils.get_db)):
    return db.query(Users).all()


# async ?
@users_router.get("/{user_id}")
async def get_user_by_userid(user_id: int, db: Session = Depends(utils.get_db)):
    return db.query(Users).filter(Users.id == user_id).first()

# async ?
@users_router.get("/get-by-email/{email}")
async def get_user_by_email(email: str, db: Session = Depends(utils.get_db)):
    return db.query(Users).filter(Users.email == email).first()


@users_router.post("/")
async def register_user(user_details: Users, db: Session = Depends(utils.get_db)):
    # split_name = user_details.name.split(" ")
    # new_user = KCUser(
    #     username=user_details.kotak_username,
    #     email=user_details.email,
    #     firstName=split_name[0],
    #     lastName=" ".join(split_name[1:]),
    # )

    # response = keycloak_utils.add_user_to_keycloak(new_user)

    # # 201 was being returned from KC, figure out a better way to handle this
    # if response["status_code"] >= 300:
    #     return response

    try:
        db.add(user_details)
        db.commit()

        return {"status": "SUCCESS", "status_code": 200}
    except Exception as e:
        # add rollback condition if DB commit fails
        return {"status": "FAILURE", "status_code": 500, "message": str(e)}
