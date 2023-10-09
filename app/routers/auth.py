from fastapi import APIRouter, Depends
from utils import utils
from models.credentials import Credentials
from models.access import UserOrgAccessResponseItem, UserOrgAccessResponse
from sqlalchemy.orm import Session

auth_router = APIRouter()

# async ?
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
@auth_router.post("/access")
async def get_access(kotak_username: str, db: Session = Depends(utils.get_db)):
    # change the argument to wrap jwt
    organization_details = await utils.get_organization_details_for_user(
        kotak_username, db
    )
    organization_details_json = []
    for organization_detail in organization_details:
        organization_details_json.append(
            UserOrgAccessResponseItem(
                path=organization_detail[0],
                name=organization_detail[1],
                access_type=organization_detail[2],
            )
        )
    organization_details_json = [
        organization_detail.__dict__
        for organization_detail in organization_details_json
    ]

    return UserOrgAccessResponse(
        kotak_username=kotak_username, access=organization_details_json
    ).__dict__
