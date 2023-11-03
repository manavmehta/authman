"""
    Utils module for authorization module.
"""
import os
import json
import jwt
import requests
import dotenv
from core import constants
from db.connection import SessionLocal
from models.organization import Organization
from models.users import Users
from models.access import UserOrgAccess
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

dotenv.load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_env_var(key):
    return os.getenv(key)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def parse_jwt(token: str):
    try:
        realm_public_key = get_public_key_by_realm("QMS")
        decoded_access_token = jwt.decode(
            token, key=realm_public_key, algorithms=["RS256"], audience="account"
        )
        return decoded_access_token
    except jwt.exceptions.ExpiredSignatureError as exception:
        raise HTTPException(
            401, {"message": "Token has expired", "exception": str(exception)}
        ) from exception
    except Exception as exception:
        raise HTTPException(
            401, {"message": "Invalid token", "exception": str(exception)}
        ) from exception


def validate_jwt(token=Depends(oauth2_scheme)):
    try:
        if token is None:
            raise HTTPException(401, "Invalid token")
        return parse_jwt(token)
    except Exception as exception:
        raise exception


def get_public_key_by_realm(realm):
    realm_url = constants.REALM_URL.format(realm)
    realm_response = requests.get(realm_url, verify=False, timeout=1000)
    public_key = json.loads(realm_response.text)["public_key"]

    return f"""-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"""


async def get_organization_details_for_user(kotak_username: str, db: Session):
    query = select(Organization.path, Organization.name, UserOrgAccess.access_type)
    query = query.join(UserOrgAccess, UserOrgAccess.organization_id == Organization.id)
    query = query.join(Users, Users.id == UserOrgAccess.user_id)
    query = query.where(Users.kotak_username == kotak_username.upper())

    return db.execute(query).all()


# Functions to be deprecated


def authenticate_user(username, password, realm_name):
    authentication_response = get_authorization_token(
        username=username, password=password, realm_name=realm_name
    )

    return {
        "status": "SUCCESS" if "error" not in authentication_response else "FAILED",
        "user_info": authentication_response,
    }


def get_authorization_token(realm_name, username, password):
    realm_client_secret = get_env_var(realm_name + "_CLIENT_SECRET")
    realm_details = constants.REALMS[realm_name]
    client_id = realm_details["CLIENT_ID"]

    payload = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_secret": realm_client_secret,
        "client_id": client_id,
    }

    try:
        realm_public_key = get_public_key_by_realm(realm_name)
        user_token_response = requests.post(
            constants.REALM_USER_TOKEN_URL.format(realm_name),
            data=payload,
            timeout=1000,
        )

        user_info = json.loads(user_token_response.text)
        user_access_token = user_info["access_token"]
        print(user_access_token)
        return jwt.decode(
            user_access_token,
            key=realm_public_key,
            algorithms=["RS256"],
            audience="account",
        )

    except KeyError as error:
        return {
            "message": f'Encountered Key Error for the key "{error.args[0]}"',
            "error": error,
        }

    except Exception as error:
        return {
            "message": "Encountered Error",
            "error": error,
        }
