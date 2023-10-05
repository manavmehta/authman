import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, UUID, ForeignKey

from db.connection import Base


class Users(Base):
    __tablename__ = "users"

    id: UUID = Column(UUID, primary_key=True)
    name: str = Column(String(100), nullable=False)
    email: str = Column(String(100), unique=True, nullable=False)
    contact_num: int = Column(Integer, nullable=False)
    supervisor_id: Optional[UUID] = Column(UUID, ForeignKey("users.id"))
    team_id: UUID = Column(UUID, ForeignKey("team.id"))
    created_at: datetime.datetime = Column()
    updated_at: datetime.datetime = Column()

    class Config:
        orm_mode = True
