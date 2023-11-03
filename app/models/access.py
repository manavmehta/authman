import datetime
from typing import List
from typing import Optional
from sqlmodel import Field, SQLModel

class UserOrgAccess(SQLModel, table=True):
    __tablename__ = "user_org_access"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    organization_id: int
    access_type: str
    created_at: Optional[datetime.datetime] = Field(default=datetime.datetime.now())
    updated_at: Optional[datetime.datetime] = Field(default=datetime.datetime.now())


class UserOrgAccessResponseItem:
    path: str
    name: str
    access_type: str

    def __init__(self, path: str, name: str, access_type: str):
        self.path = path
        self.name = name
        self.access_type = access_type


class UserOrgAccessResponse:
    access: List[UserOrgAccessResponseItem]
    kotak_username: str

    def __init__(self, kotak_username: str, access: List[UserOrgAccessResponseItem]):
        self.kotak_username = kotak_username
        self.access = access

    def __json__(self):
        return {"kotak_username": self.kotak_username, "access": self.access}
