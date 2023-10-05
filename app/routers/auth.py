from fastapi import APIRouter
from utils import utils
from models.credentials import Credentials

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
