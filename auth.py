"""
    Authorization module that will act as middleware to authenticate the user to QMS.
"""
from pprint import pprint
import utils

username, password = input("username:"), input("password:")

authentication_response = utils.authenticate_user(
    username=username, password=password, realm_name="QMS"
)

authentication_status = authentication_response["status"]

pprint(
    {
        "authentication_status": authentication_status,
        "authentication_response": authentication_response,
    }
)

if authentication_status.lower() == "success":
    pprint(utils.check_authorization(username=username, realm_name="QMS"))
