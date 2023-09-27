"""
    Authorization module that will act as middleware to authenticate the user to QMS.
"""
from pprint import pprint
import utils

username, password = input("username:"), input("password:")

authentication_response = utils.authenticate_user(
    username=username, password=password, realm_name="QMS"
)

pprint(authentication_response)
