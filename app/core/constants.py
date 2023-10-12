"""
    constants for the middleware
"""

REALM_URL = "http://localhost:18080/auth/realms/{0}"

REALM_USER_TOKEN_URL = (
    "http://localhost:18080/auth/realms/{0}/protocol/openid-connect/token"
)
BRUTE_FORCE_USERS_URL = (
    "http://localhost:18080/auth/admin/realms/{0}/ui-ext/brute-force-user"
)

CONTENT_TYPE_APPLICATION_JSON = "application/json"
REALMS = {
    "QMS": {
        "CLIENT_ID": "qms",
        "REALM_NAME": "QMS",
        "CLIENT_ID_CODE": "dc7f78ff-6a45-415a-bf79-1a7b06a76b3e",
    }
}

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/authman"
KEYCLOAK_USERS_URL = "http://localhost:18080/auth/admin/realms/QMS/users"
KEYCLOAK_AUTH_ADMIN = (
    "http://localhost:18080/auth/realms/QMS/protocol/openid-connect/token"
)
