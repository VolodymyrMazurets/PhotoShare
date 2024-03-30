from fastapi import APIRouter, File, UploadFile, Depends
from typing import List
from sqlalchemy.orm import Session
from src.models import User
from src.core.db import get_db
from src.schemas.posts import PostCreate, PostUpdate, PostDelete, PostModelWithImage, PostModelCreate, PostTransformImage, PostTransformImageQR
from src.crud.post import upload_post_with_description, delete_post, update_post_description, get_post_by_id, get_posts_list, get_own_posts_list, transform_image, generate_and_get_qr_code
from src.services.auth import auth_service

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[PostModelWithImage])
async def get_all_own_posts(user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    return await get_own_posts_list(user, db)


@router.get("/all", response_model=List[PostModelWithImage])
async def get_all_posts(db: Session = Depends(get_db)):
    return await get_posts_list(db)


@router.post("/", response_model=PostCreate)
async def upload_post(user: User = Depends(auth_service.get_current_user), image: UploadFile = File(...), body: PostModelCreate = Depends(PostModelCreate), db: Session = Depends(get_db)):
    post = await upload_post_with_description(user, image, body, db)
    return {"post": post, "detail": "Post successfully created"}


@router.delete("/{post_id}", response_model=PostDelete)
async def remove_post(post_id: int, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    post = await delete_post(post_id, user, db)
    return {"detail": 'Post successfully deleted'}


@router.patch("/{post_id}", response_model=PostUpdate)
async def update_post(post_id: int, description: str, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    post = await update_post_description(post_id, description, user, db)
    return {"post": post, "detail": 'Post successfully updated'}


@router.get("/{post_id}", response_model=PostModelWithImage)
async def get_specific_post(post_id: int, db: Session = Depends(get_db)):
    return await get_post_by_id(post_id, db)


@router.post("/transform/{post_id}", response_model=PostTransformImage)
async def transform_post_image(post_id: int, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db), gravity: str | None = None, height: int | None = None, width: int | None = None, radius: str | None = None):
    image =  await transform_image(post_id, user, db, gravity, height, width, radius)
    return {"image": image, "detail": "Post image successfully transformed"}


@router.post("/qr/{post_id}", response_model=PostTransformImageQR)
async def transform_post_image(post_id: int, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    qr = await generate_and_get_qr_code(post_id, user, db)
    return {"image": qr, "detail": "QR code successfully generated"}
