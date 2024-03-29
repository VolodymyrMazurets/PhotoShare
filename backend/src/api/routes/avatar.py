from fastapi import APIRouter, Depends, UploadFile, File
from src.crud import users as repository_users
from src.schemas.users import UserDb
from sqlalchemy.orm import Session
from src.models import User
from src.services.auth import auth_service
from src.core.db import get_db
import cloudinary
import cloudinary.uploader
from src.core.config import settings

router = APIRouter(prefix="/avatar", tags=["avatar"])

@router.patch('/', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'photo_share/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'photo_share/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
