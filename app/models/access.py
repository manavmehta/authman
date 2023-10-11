import datetime
from sqlalchemy import Column, Integer, ForeignKey, Enum

from pydantic import BaseModel
from db.connection import Base


class UserOrgAccess(Base):
    __tablename__ = "user_org_access"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    access_type = Column(Enum("R", "W"), nullable=False)

    created_at: datetime.datetime = Column()
    updated_at: datetime.datetime = Column()

    class Config:
        orm_mode = True


class UserOrgAccessRequest(BaseModel):
    access_token: str
    token_type: str
    session_state: str
    scope: str


class UserOrgAccessResponseItem:
    path: str
    name: str
    access_type: str

    def __init__(self, path: str, name: str, access_type: str):
        self.path = path
        self.name = name
        self.access_type = access_type

    def __json__(self):
        return {"path": self.path, "name": self.name, "access_type": self.access_type}


class UserOrgAccessResponse:
    access: list[UserOrgAccessResponseItem]
    kotak_username: str

    def __init__(self, kotak_username: str, access: list[UserOrgAccessResponseItem]):
        self.kotak_username = kotak_username
        self.access = access

    def __json__(self):
        return {"kotak_username": self.kotak_username, "access": self.access}
