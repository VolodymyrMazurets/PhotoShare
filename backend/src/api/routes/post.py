from fastapi import APIRouter, File, UploadFile, Depends
from typing import List
from sqlalchemy.orm import Session
from src.models import User
from src.core.db import get_db
from src.schemas.posts import PostCreate, PostUpdate, PostDelete, PostModelWithImage, PostModelCreate
from src.crud.post import upload_post_with_description, delete_post, update_post_description, get_post_by_id, get_posts_list
from src.services.auth import auth_service

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[PostModelWithImage])
async def get_all_posts(db: Session = Depends(get_db)):
    return await get_posts_list(db)


@router.post("/", response_model=PostCreate)
async def upload_post(user: User = Depends(auth_service.get_current_user), image: UploadFile = File(...), body: PostModelCreate = Depends(PostModelCreate), db: Session = Depends(get_db)):
    post = await upload_post_with_description(user, image, body, db)
    return {"post": post, "detail": "Post successfully created"}


@router.delete("/{post_id}", response_model=PostDelete)
async def delete_post(post_id: int, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    post = await delete_post(post_id, user, db)
    return {"post": post, "detail": 'Post successfully deleted'}


@router.patch("/{post_id}", response_model=PostUpdate)
async def update_post_description(post_id: int, description: str, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    post = await update_post_description(post_id, description, user, db)
    return {"post": post, "detail": 'Post successfully updated'}


@router.get("/{post_id}", response_model=PostModelWithImage)
async def get_specific_post(post_id: int, db: Session = Depends(get_db)):
    return await get_post_by_id(post_id, db)
