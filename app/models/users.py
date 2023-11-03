import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Users(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    contact_num: int
    kotak_username: str
    supervisor_id: Optional[int] = -1
    organization_id: int
    created_at: Optional[datetime.datetime] = Field(default=datetime.datetime.now())
    updated_at: Optional[datetime.datetime] = Field(default=datetime.datetime.now())
