"""
    Authorization module that will act as middleware to authenticate the user to QMS.
"""
import uvicorn
from fastapi import FastAPI
from api import authman_router

authman = FastAPI()

authman.include_router(authman_router, prefix="/api", tags=["authman"])

# uvicorn.run("main:app", host="127.0.0.1", port=8008, reload=True)

# uvicorn.run("main:authman", reload=True)
