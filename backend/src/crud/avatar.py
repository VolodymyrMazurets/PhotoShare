
import cloudinary
import cloudinary.uploader

from fastapi import File, status, HTTPException
from sqlalchemy.orm import Session

from src.models import User
from src.core.config import settings
from src.crud.users import update_avatar as update_ava
from src.constants.messages import BAD_REQUEST


async def update_avatar(file: File, current_user: User, db: Session):
    try:
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True
        )

        r = cloudinary.uploader.upload(
            file.file, public_id=f'photo_share/{current_user.username}', overwrite=True)
        src_url = cloudinary.CloudinaryImage(f'photo_share/{current_user.username}')\
            .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=BAD_REQUEST)
    return await update_ava(current_user.email, src_url, db)
