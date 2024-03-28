from fastapi import File
import uuid
import cloudinary
import cloudinary.uploader
from sqlalchemy import and_
from sqlalchemy.orm import Session


from src.models import Post, User
from src.schemas.posts import PostModel
from src.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


async def upload_post_with_description(user: User, image: File, body: PostModel,  db: Session):
    try:
        public_id = f"photo_share/{uuid.uuid4()}"
        upload_result = cloudinary.uploader.upload(
            image.file, public_id=public_id)
        res_url = cloudinary.CloudinaryImage(public_id).build_url(
            version=upload_result.get("version")
        )
        post = Post(title=body.title, description=body.description,
                    image=res_url, user_id=user.id)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except Exception as e:
        print(e)


async def delete_post(post_id: int, user: User, db: Session):
    try:
        post = db.query(Post).filter(
            and_(Post.user_id == user.id, Post.id == post_id)).first()
        if post:
            cloudinary.uploader.destroy(post.image)
            db.delete(post)
            db.commit()
            return post
    except Exception as e:
        print(e)


async def update_post_description(post_id: int, description: str, user: User, db: Session):
    try:
        post = db.query(Post).filter(
            and_(Post.user_id == user.id, Post.id == post_id)).first()
        if post:
            post.description = description
            db.commit()
            return post
    except Exception as e:
        print(e)


async def get_post_by_id(post_id: int, db: Session):
    try:
        post = db.query(Post).filter(
            Post.id == post_id).first()
        return post
    except Exception as e:
        print(e)
