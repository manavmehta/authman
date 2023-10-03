"""
    Utils module for authorization module.
"""
import os
import json
import jwt
import requests
import dotenv
from core import constants

from pprint import pprint

dotenv.load_dotenv()


def get_env_var(key):
    return os.getenv(key)


"""
    The below functions are being used for authentication purposes
"""


def authenticate_user(username, password, realm_name):
    authentication_response = get_authorization_token(
        username=username, password=password, realm_name=realm_name
    )

    pprint(authentication_response)

    return {
        "status": "SUCCESS" if "error" not in authentication_response else "FAILED",
        "user_info": authentication_response,
    }


def get_public_key_by_realm(realm):
    realm_url = constants.REALM_URL.format(realm)
    realm_response = requests.get(realm_url, verify=False, timeout=1000)
    public_key = json.loads(realm_response.text)["public_key"]

    return f"""-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"""


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

        return jwt.decode(user_access_token, key=realm_public_key, algorithms=["RS256"])

    except KeyError as error:
        return {
            "message": f'Encountered Key Error for the key "{error.args[0]}"',
            "error": error,
        }
    except Exception as error:
        return {
            "message": f'Encountered Error',
            "error": error,
        }
