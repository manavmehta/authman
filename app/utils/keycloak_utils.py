import json
import requests
from core import constants
from models.keycloak import KCUser
from utils import utils

def add_user_to_keycloak(user_details: KCUser):
    url = constants.KEYCLOAK_USERS_URL

    payload = json.dumps(user_details.__dict__)
    admin_details, status_code = get_admin_token()

    if status_code >= 300:
        return {'status': "FAILED", "status_code": status_code, "error": admin_details}

    admin_access_token = admin_details['access_token']
    headers = {
        "authorization": f"""Bearer {admin_access_token}""",
        "content-type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload, timeout=60)

    if response.status_code >= 300:
        return {'status': "FAILED", "status_code": response.status_code, "error": response.text}

    return {'status': "SUCCESS", "status_code": 200, "response": response.text}

def get_admin_token():

    url = constants.KEYCLOAK_AUTH_ADMIN

    admin_username = utils.get_env_var("QMS_ADMIN_USERNAME")
    admin_password = utils.get_env_var("QMS_ADMIN_PASSWORD")
    client_secret = utils.get_env_var("QMS_CLIENT_SECRET")

    payload = {
    "grant_type": "password",
    "client_id": "admin-cli",
    "username": admin_username,
    "password": admin_password,
    "client_secret" : client_secret,
    }
    headers = {
    'Content-type': 'application/x-www-form-urlencoded',
    }

    response = requests.request("POST", url, headers=headers, data=payload, timeout=60)
    return json.loads(response.text), response.status_code
