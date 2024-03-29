from fastapi import APIRouter

from src.api.routes import auth, comments, post, profile, avatar

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(comments.router, tags=["comments"])
api_router.include_router(post.router, tags=["posts"])
api_router.include_router(profile.router, tags=["profile"])
api_router.include_router(avatar.router, tags=["avatar"])


