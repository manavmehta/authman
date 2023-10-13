from os import environ
"""
    constants for the middleware
"""

KEYCLOAK_BASE_URL = environ.get("KEYCLOAK_BASE_URL", "http://localhost:18080/auth")
POSTGRES_HOST = environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = environ.get("POSTGRES_DB", "authman")
POSTGRES_USERNAME = environ.get("POSTGRES_USERNAME", "postgres")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD", "postgres")



# Keycloak specific URLs
REALM_URL =  f"{KEYCLOAK_BASE_URL}/realms/{0}"
REALM_USER_TOKEN_URL = f"{KEYCLOAK_BASE_URL}/realms/{0}/protocol/openid-connect/token"
BRUTE_FORCE_USERS_URL = f"{KEYCLOAK_BASE_URL}/admin/realms/{0}/ui-ext/brute-force-user"
KEYCLOAK_USERS_URL = f"{KEYCLOAK_BASE_URL}/admin/realms/QMS/users"
KEYCLOAK_AUTH_ADMIN = f"{KEYCLOAK_BASE_URL}/realms/QMS/protocol/openid-connect/token"

# Postgres configuration
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


# Extra constants
CONTENT_TYPE_APPLICATION_JSON = "application/json"

REALMS = {
    "QMS": {
        "CLIENT_ID": "qms",
        "REALM_NAME": "QMS",
        "CLIENT_ID_CODE": "dc7f78ff-6a45-415a-bf79-1a7b06a76b3e",
    }
}
