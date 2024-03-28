import json
from fastapi import File, HTTPException
import uuid
import cloudinary
import cloudinary.uploader
from sqlalchemy import and_
from sqlalchemy.orm import Session


from src.models import Post, User, Tag
from src.schemas.posts import PostModelCreate
from src.core.config import settings
from src.crud.tags import create_tag_if_not_exist

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


async def upload_post_with_description(user: User, image: File, body: PostModelCreate,  db: Session):
    if len(body.tags) > 5:
        raise HTTPException(status_code=400, detail="Tags must be less than 5")
    try:
        tags = body.tags[0].split(",") if len(body.tags) > 0 else []
        tags_ids = []
        for tag in tags:
            t = create_tag_if_not_exist(tag, db)
            tags_ids.append(t.id)

        tags_from_db = db.query(Tag).filter(Tag.id.in_(tags_ids)).all()

        public_id = f"photo_share/{uuid.uuid4()}"
        upload_result = cloudinary.uploader.upload(
            image.file, public_id=public_id)
        res_url = cloudinary.CloudinaryImage(public_id).build_url(
            version=upload_result.get("version")
        )
        post = Post(title=body.title, description=body.description,
                    image=res_url, user_id=user.id, tags=tags_from_db)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except Exception as e:
        print(e)


async def delete_post(post_id: int, user: User, db: Session):
    post = db.query(Post).filter(
        and_(Post.user_id == user.id, Post.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    cloudinary.uploader.destroy(post.image)
    db.delete(post)
    db.commit()
    return post


async def update_post_description(post_id: int, description: str, user: User, db: Session):
    post = db.query(Post).filter(
        and_(Post.user_id == user.id, Post.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.description = description
    db.commit()
    return post


async def get_post_by_id(post_id: int, db: Session):
    post = db.query(Post).filter(
        Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
