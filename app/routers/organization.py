from fastapi import APIRouter, Depends
from models.organization import Organization
from sqlalchemy.orm import Session
from utils import utils

organization_router = APIRouter()

# async ?
@organization_router.get("/")
async def get_organization(org_id: int, db: Session = Depends(utils.get_db)):
    return db.query(Organization).filter(Organization.id == org_id).first()
