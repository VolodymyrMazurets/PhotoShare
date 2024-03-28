from fastapi import APIRouter

from src.api.routes import auth, comments

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(comments.router, tags=["comments"])
