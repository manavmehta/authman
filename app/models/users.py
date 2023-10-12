import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey

from pydantic import BaseModel
from db.connection import Base


class Users(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(100), nullable=False)
    email: str = Column(String(100), unique=True, nullable=False)
    contact_num: int = Column(Integer, nullable=False)
    kotak_username: str = Column(String, nullable=False)
    supervisor_id: Optional[int] = Column(Integer, ForeignKey("users.id"))
    organization_id: int = Column(Integer, ForeignKey("organization.id"))
    created_at: datetime.datetime = Column(default=datetime.datetime.now())
    updated_at: datetime.datetime = Column(default=datetime.datetime.now())

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: str
    contact_num: int
    kotak_username: str
    supervisor_id: int
    organization_id: int
