from fastapi import APIRouter, File, UploadFile
from src.models import Post
import cloudinary
import cloudinary.uploader
from src.crud.post import upload_image_with_description, delete_image, update_image_description, get_image_by_id

router = APIRouter()


async def upload_image_with_description(user_id: int, image_data: bytes, description: str):
    cloudinary_response = cloudinary.uploader.upload(image_data)
    image_url = cloudinary_response.get("secure_url")
    new_post = Post(user_id=user_id, description=description, image=image_url)
    await new_post.save()
    
    return {"message": "Image uploaded successfully with description"}

@router.delete("/delete-image/{image_id}")
async def delete_image_route(image_id: int):
    return await delete_image(image_id)

@router.put("/update-image-description/{image_id}")
async def update_image_description_route(image_id: int, description: str):
    return await update_image_description(image_id, description)

@router.get("/get-image/{image_id}")
async def get_image_route(image_id: int):
    return await get_image_by_id(image_id)