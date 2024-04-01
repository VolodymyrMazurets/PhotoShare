import uuid
import cloudinary
import cloudinary.uploader
from tempfile import NamedTemporaryFile
from qrcode import QRCode
from fastapi import File, HTTPException, status
from sqlalchemy.orm import Session

from src.models import Post, User, Tag
from src.schemas.posts import PostModelCreate
from src.core.config import settings
from src.crud.tags import create_tag_if_not_exist
from src.constants.messages import UNPROCESSABLE_ENTITY, BAD_REQUEST, POST_NOT_FOUND, OPERATION_FORBIDDEN, POST_NO_TRANSFORMED_IMAGE

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


async def upload_post_with_description(user: User, image: File, body: PostModelCreate,  db: Session):
    if len(body.tags) > 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=UNPROCESSABLE_ENTITY)
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=BAD_REQUEST)


async def delete_post(post_id: int, user: User, db: Session):
    post = await get_post_by_id(post_id, db)
    check_permission(user.role, post.user_id, user.id)
    try:
        if post.image_public_id:
            cloudinary.uploader.destroy(post.image_public_id)
        db.delete(post)
        db.commit()
        return post
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=BAD_REQUEST)


async def update_post_description(post_id: int, description: str, user: User, db: Session):
    post = await get_post_by_id(post_id, db)
    check_permission(user.role, post.user_id, user.id)
    try:
        post.description = description
        db.commit()
        db.refresh(post)
        return post
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=BAD_REQUEST)


async def get_post_by_id(post_id: int, db: Session):
    post = db.query(Post).filter(
        Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=POST_NOT_FOUND)
    return post


async def get_posts_list(db: Session):
    try:
        return db.query(Post).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=BAD_REQUEST)


async def get_own_posts_list(user: User, db: Session):
    try:
        return db.query(Post).filter(user.id == Post.user_id).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=BAD_REQUEST)


async def transform_image(post_id: int, user: User, db: Session, gravity: str | None = None, height: int | None = None, width: int | None = None, radius: str | None = None):
    post = await get_post_by_id(post_id, db)
    check_permission(user.role, post.user_id, user.id)
    try:
        transformed_image_url = cloudinary.CloudinaryImage(post.image_public_id).build_url(transformation=[
            {'gravity': gravity, 'height': height,
                'width': width, 'crop': "thumb"},
            {'radius': radius},
            {'fetch_format': "auto"}
        ])
        post.transformed_image = transformed_image_url
        db.commit()
        db.refresh(post)
        return post.transformed_image
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=BAD_REQUEST)


def create_qr_code(url: str):
    try:
        qr = QRCode(version=3, box_size=20, border=10)
        qr_data = url
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_temp_file = NamedTemporaryFile(delete=True)
        qr_img.save(qr_temp_file.name)
        return qr_temp_file
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=BAD_REQUEST)


async def generate_and_get_qr_code(post_id: int, user: User, db: Session):
    post = await get_post_by_id(post_id, db)
    check_permission(user.role, post.user_id, user.id)
    if not post.transformed_image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=POST_NO_TRANSFORMED_IMAGE)
    qr_temp_file = create_qr_code(post.transformed_image)
    try:
        upload_result = cloudinary.uploader.upload(
            qr_temp_file.file, public_id=post.image_public_id + "_qr")
        upload_result_url = cloudinary.CloudinaryImage(
            post.image_public_id + "_qr").build_url(version=upload_result.get("version"))
        post.transformed_image_qr = upload_result_url
        db.commit()
        db.refresh(post)
        return post.transformed_image_qr
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=BAD_REQUEST)


def check_permission(user_role, post_user_id, current_user_id):
    if user_role not in ['admin', 'moderator'] and post_user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=OPERATION_FORBIDDEN
        )
