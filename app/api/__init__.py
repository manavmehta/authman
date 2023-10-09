from fastapi import APIRouter
from routers.auth import auth_router
from routers.users import users_router
from routers.organization import organization_router

v1_router = APIRouter()

v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(users_router, prefix="/users", tags=["users"])
v1_router.include_router(organization_router, prefix="/org", tags=["organization"])
