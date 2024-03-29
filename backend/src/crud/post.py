from tempfile import NamedTemporaryFile
from qrcode import QRCode
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
                    image=res_url, user_id=user.id, tags=tags_from_db, image_public_id=public_id)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except Exception as e:
        print(e)


async def delete_post(post_id: int, user: User, db: Session):
    if user.role == 'admin':
        post = db.query(Post).filter(
            and_(Post.id == post_id)).first()
    else:
        post = db.query(Post).filter(
            and_(Post.id == post_id, Post.user_id == user.id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    cloudinary.uploader.destroy(post.image)
    db.delete(post)
    db.commit()
    return post


async def update_post_description(post_id: int, description: str, user: User, db: Session):
    if user.role == 'admin':
        post = db.query(Post).filter(
            and_(Post.id == post_id)).first()
    else:
        post = db.query(Post).filter(
            and_(Post.id == post_id, Post.user_id == user.id)).first()

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


async def get_posts_list(db: Session):
    posts = db.query(Post).all()
    return posts


async def get_own_posts_list(user: User, db: Session):
    posts = db.query(Post).filter(user.id == Post.user_id).all()
    return posts


async def transform_image(post_id: int, user: User, db: Session, gravity: str | None = None, height: int | None = None, width: int | None = None, radius: str | None = None):
    post = await get_post_by_id(post_id, db)
    if (post):
        transformed_image_url = cloudinary.CloudinaryImage(post.image_public_id).build_url(transformation=[
            {'gravity': gravity, 'height': height,
                'width': width, 'crop': "thumb"},
            {'radius': radius},
            {'fetch_format': "auto"}
        ])

        qr = QRCode(version=3, box_size=20, border=10)
        data = transformed_image_url
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        temp_file = NamedTemporaryFile(delete=True)
        img.save(temp_file.name)
        upload_result = cloudinary.uploader.upload(
            temp_file.file, public_id=post.image_public_id + "_qr")
        res_url = cloudinary.CloudinaryImage(post.image_public_id + "_qr").build_url(
            version=upload_result.get("version")
        )
        post.transformed_image = transformed_image_url
        post.transformed_image_qr = res_url
        db.commit()
        return post
