import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text

from pydantic import BaseModel
from db.connection import Base


class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("organization.id"))
    name = Column(String(100), nullable=False)
    path = Column(Text)
    created_at: datetime.datetime = Column(default=datetime.datetime.now())
    updated_at: datetime.datetime = Column(default=datetime.datetime.now())

    class Config:
        orm_mode = True


class OrgCreate(BaseModel):
    name: str
    parent_id: int
