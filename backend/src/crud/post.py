from fastapi import File
from src.models import Post, User
from src.schemas.posts import PostModel
from src.core.config import settings
import uuid
import cloudinary

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


async def upload_image_with_description(body: PostModel, user: User, image: File,):
    try:
        public_id = f"photo_share/{uuid.uuid4()}"
        upload_result = cloudinary.uploader.upload(
            image.file, public_id=public_id)
        res_url = cloudinary.CloudinaryImage(public_id).build_url(
            width=250, height=250, crop="fill", version=upload_result.get("version")
        )
        image = Post(title=body.title, description=body.description,
                     image=res_url, user_id=user.id)
        await image.save()
        return image
    except Exception as e:
        return {"message": f"Failed to upload image: {str(e)}"}


async def delete_image(image_id: int):
    try:
        image = await Post.get(id=image_id)
        deletion_result = cloudinary.uploader.destroy(image.url)
        await image.delete()
        return {"message": f"Image with ID {image_id} deleted successfully"}
    except Exception as e:
        return {"message": f"Failed to delete image: {str(e)}"}


async def update_image_description(image_id: int, description: str):
    try:
        image = await Post.get(id=image_id)
        image.description = description
        await image.save()
        return {"message": f"Description for image with ID {image_id} updated successfully"}
    except Exception as e:
        return {"message": f"Failed to update image description: {str(e)}"}


async def get_image_by_id(image_id: int):
    try:
        image = await Post.get(id=image_id)
        return {"id": image.id, "url": image.url, "description": image.description}
    except Exception as e:
        return {"message": f"Failed to get image by ID: {str(e)}"}
