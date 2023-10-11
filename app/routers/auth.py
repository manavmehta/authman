from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils import utils
from models.credentials import Credentials
from models.access import (
    UserOrgAccessResponseItem,
    UserOrgAccessRequest,
    UserOrgAccessResponse,
)
import jwt

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
# current issue: JWT refreshes fast, so withing a couple of minutes,
# there will be a backend error -> jwt.exceptions.ExpiredSignatureError: Signature has expired
@auth_router.post("/access")
async def get_authorization(
    request: UserOrgAccessRequest, db: Session = Depends(utils.get_db)
):
    try:
        access_token = request.access_token
        realm_public_key = utils.get_public_key_by_realm("QMS")
        decoded_access_token = jwt.decode(
            access_token, key=realm_public_key, algorithms=["RS256"], audience="account"
        )

        organization_details = await utils.get_organization_details_for_user(
            decoded_access_token["preferred_username"], db
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
            kotak_username=decoded_access_token["preferred_username"],
            access=organization_details_json,
        ).__dict__
    except jwt.exceptions.ExpiredSignatureError:
        return {"status": "FAILED", "message": "Token has expired"}
