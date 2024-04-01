from fastapi import APIRouter, Depends, UploadFile, File
from fastapi_limiter.depends import RateLimiter
from src.crud.avatar import update_avatar
from src.schemas.users import UserDb
from sqlalchemy.orm import Session
from src.models import User
from src.services.auth import auth_service
from src.core.db import get_db


router = APIRouter(prefix="/avatar", tags=["avatar"])


@router.patch('/', response_model=UserDb, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    return await update_avatar(file, current_user, db)
