from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from utils import utils
from models.credentials import Credentials
from models.access import (
    UserOrgAccessResponseItem,
    UserOrgAccessResponse,
)

auth_router = APIRouter()


# async ?
# To be deprecated
@auth_router.post("/")
async def authenticate(credentials: Credentials):
    """
    Authorization module that will act as middleware to authenticate the user to QMS.
    """

    authentication_response = utils.authenticate_user(
        username=credentials.username, password=credentials.password, realm_name="QMS"
    )

    return authentication_response


# async ?
@auth_router.get("/access")
async def get_authorization(
    access_token: str = Depends(utils.validate_jwt),
    db: Session = Depends(utils.get_db),
):
    try:
        access_reponse = await utils.get_organization_details_for_user(
            access_token["preferred_username"], db
        )

        return UserOrgAccessResponse(
            kotak_username=access_token["preferred_username"],
            access=[
                UserOrgAccessResponseItem(
                    path=organization_detail[0],
                    name=organization_detail[1],
                    access_type=organization_detail[2],
                )
                for organization_detail in access_reponse
            ],
        )
    except HTTPException as exception:
        return {"status": "FAILED", "message": str(exception)}
    except Exception as exception:
        return {"status": "FAILED", "message": str(exception)}
