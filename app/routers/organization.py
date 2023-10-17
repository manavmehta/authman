from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.organization import Organization, OrgCreate
from utils import utils

organization_router = APIRouter()


# async ?
@organization_router.get("/")
async def get_organization(org_id: int, db: Session = Depends(utils.get_db)):
    return db.query(Organization).filter(Organization.id == org_id).first()


@organization_router.post("/")
async def register_org(org_details: OrgCreate, db: Session = Depends(utils.get_db)):
    try:
        new_user = Organization(
            name=org_details.name,
            parent_id=org_details.parent_id,
        )

        db.add(new_user)
        db.commit()

        return {"status": "SUCCESS", "status_code": 200}
    except Exception as e:
        return {"status": "FAILURE", "status_code": 500, "message": str(e)}


@organization_router.put("/{org_id}")
async def update_org_by_id(
    org_id: int, org_details: OrgCreate, db: Session = Depends(utils.get_db)
):
    try:
        org = db.query(Organization).filter(Organization.id == org_id).first()

        if org is None:
            return {
                "status": "FAILURE",
                "status_code": 404,
                "message": "Organization not found",
            }

        org.name = org_details.name
        org.parent_id = org_details.parent_id

        db.commit()

        return {"status": "SUCCESS", "status_code": 200}
    except Exception as e:
        return {"status": "FAILURE", "status_code": 500, "message": str(e)}


@organization_router.delete("/{org_id}")
async def delete_org_by_id(org_id: int, db: Session = Depends(utils.get_db)):
    try:
        org = db.query(Organization).filter(Organization.id == org_id).first()

        if org is None:
            return {
                "status": "FAILURE",
                "status_code": 404,
                "message": "Organization not found",
            }

        db.delete(org)
        db.commit()

        return {"status": "SUCCESS", "status_code": 200}
    except Exception as e:
        return {"status": "FAILURE", "status_code": 500, "message": str(e)}
