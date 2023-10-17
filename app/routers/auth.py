from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils import utils
from models.credentials import Credentials
from models.access import (
    UserOrgAccessResponseItem,
    UserOrgAccessResponse,
)
import jwt

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
    access_token: str = Depends(utils.oauth2_scheme),
    db: Session = Depends(utils.get_db),
):
    try:
        realm_public_key = utils.get_public_key_by_realm("QMS")

        decoded_access_token = jwt.decode(
            access_token, key=realm_public_key, algorithms=["RS256"], audience="account"
        )

        access_reponse = await utils.get_organization_details_for_user(
            decoded_access_token["preferred_username"], db
        )

        return UserOrgAccessResponse(
            kotak_username=decoded_access_token["preferred_username"],
            access=[
                UserOrgAccessResponseItem(
                    path=organization_detail[0],
                    name=organization_detail[1],
                    access_type=organization_detail[2],
                )
                for organization_detail in access_reponse
            ],
        )
    except jwt.exceptions.ExpiredSignatureError:
        return {"status": "FAILED", "message": "Token has expired"}
    except Exception as e:
        return {"status": "FAILED", "message": str(e)}
