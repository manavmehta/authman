"""
    Utils module for authorization module.
"""
import os
import json
import dotenv
import constants
import requests
import jwt

dotenv.load_dotenv()


def get_env_var(key):
    return os.getenv(key)


"""
    The below functions are being used for authentication purposes and will be combined with authorization functions above
"""


def authenticate_user(username, password, realm_name):
    authentication_response = get_authorization_token(
        username=username, password=password, realm_name=realm_name
    )

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
    realm_client_secret = os.getenv(realm_name + "_CLIENT_SECRET")
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
        return error


"""
    The below functions are being used for authorization
"""


def check_authorization(username, realm_name):
    admin_access_variables = get_admin_access_token_by_realm(realm_name)

    admin_auth_token = f"{admin_access_variables['token_type']} {admin_access_variables['access_token']}"

    username_id_mapping = get_users_from_realm(
        constants.REALMS[realm_name]["REALM_NAME"], admin_auth_token
    )

    response = get_permit_status_by_userId_and_realm(
        userId=username_id_mapping[username],
        realm_name=realm_name,
        admin_auth=admin_auth_token,
    )

    return {"username": username, "access": response}


def parse_authorization_response(response):
    parsed_response = json.loads(response.text)

    return (
        parsed_response
        if "error" in parsed_response
        else {
            obj["resource"]["name"]: obj["status"]
            for obj in parsed_response.get("results", [])
        }
    )


def get_permit_status_by_userId_and_realm(userId, realm_name, admin_auth):
    realm_details = constants.REALMS[realm_name]
    evaluate_url = constants.EVALUATE_URL.format(
        realm_details["REALM_NAME"], realm_details["CLIENT_ID_CODE"]
    )
    payload = json.dumps({"userId": userId})
    headers = {
        "authorization": admin_auth,
        "content-type": constants.CONTENT_TYPE_APPLICATION_JSON,
    }

    response = requests.post(evaluate_url, headers=headers, data=payload, timeout=1000)

    return parse_authorization_response(response)


def get_admin_access_token_by_realm(realm_name):
    url = constants.REALM_USER_TOKEN_URL.format(realm_name)
    realm_details = constants.REALMS[realm_name]

    admin_username, admin_password = get_env_var(
        realm_name + "_ADMIN_USERNAME"
    ), get_env_var(realm_name + "_ADMIN_PASSWORD")

    realm_client_secret = os.getenv(realm_name + "_CLIENT_SECRET")

    payload = {
        "grant_type": "password",
        "client_id": realm_details["CLIENT_ID"],
        "client_secret": realm_client_secret,
        "username": admin_username,
        "password": admin_password,
    }

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    response = requests.post(url, headers=headers, data=payload, timeout=1000)

    return json.loads(response.text)


def parse_brute_force_users(users_response):
    return {user["username"]: user["id"] for user in users_response}


def get_users_from_realm(realm_name, admin_auth):
    realm_details = constants.REALMS[realm_name]

    url = constants.BRUTE_FORCE_USERS_URL.format(realm_details["REALM_NAME"])

    headers = {"Authorization": admin_auth}

    response = requests.get(url, headers=headers, timeout=1000)

    return parse_brute_force_users(json.loads(response.text))
