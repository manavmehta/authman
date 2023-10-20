from fastapi import APIRouter
from routers.auth import auth_router
from routers.users import users_router
from routers.organization import organization_router

authman_router = APIRouter()

authman_router.include_router(auth_router, prefix="/auth", tags=["auth"])
authman_router.include_router(users_router, prefix="/users", tags=["users"])
authman_router.include_router(organization_router, prefix="/org", tags=["organization"])
