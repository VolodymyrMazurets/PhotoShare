from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from src.models import Post, User
from src.core.db import get_db
from src.schemas.posts import PostCreate, PostUpdate, PostDelete, PostModel, PostModelWithImage
from src.crud.post import upload_post_with_description, delete_post, update_post_description, get_post_by_id
from src.services.auth import auth_service

router = APIRouter()


@router.post("/upload-post", response_model=PostCreate)
async def upload_post_route(user: User = Depends(auth_service.get_current_user), image: UploadFile = File(...), body: PostModel = Depends(PostModel), db: Session = Depends(get_db)):
    post = await upload_post_with_description(user, image, body, db)
    return {"post": post, "detail": "Post successfully created"}


@router.delete("/delete-post/{post_id}", response_model=PostDelete)
async def delete_post_route(post_id: int, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    post = await delete_post(post_id, user, db)
    return {"post": post, "detail": 'Post successfully deleted'}


@router.patch("/update-post-description/{post_id}", response_model=PostUpdate)
async def update_post_description_route(post_id: int, description: str, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    post = await update_post_description(post_id, description, user, db)
    return {"post": post, "detail": 'Post successfully updated'}


@router.get("/get-post/{post_id}", response_model=PostModelWithImage)
async def get_image_route(post_id: int, db: Session = Depends(get_db)):
    return await get_post_by_id(post_id, db)
     
