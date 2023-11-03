import datetime
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Organization(SQLModel, table=True):
    __tablename__ = "organization"

    id: Optional[int] = Field(default=None, primary_key=True)
    parent_id: Optional[int] = -1
    name: str
    path: Optional[str]
    created_at: Optional[datetime.datetime] = Field(default=datetime.datetime.now())
    updated_at: Optional[datetime.datetime] = Field(default=datetime.datetime.now())


class OrgCreate(BaseModel):
    name: str
    parent_id: Optional[int]
