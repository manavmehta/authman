from pydantic import BaseModel


class KCUser(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    requiredActions: list = []
    emailVerified: bool = True
    groups: list = []
    enabled: bool = True

    def __json__(self):
        return {
            "username": self.kotak_username,
            "email": self.email,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "requiredActions": self.requiredActions,
            "emailVerified": self.emailVerified,
            "groups": self.groups,
            "enabled": self.enabled,
        }
