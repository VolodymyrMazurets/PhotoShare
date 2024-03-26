from fastapi import APIRouter, UploadFile
from src.services.image_service import upload_image_with_description, delete_image, update_image_description, get_image_by_id

router = APIRouter()

@router.post("/upload-image")
async def upload_image(image: UploadFile, description: str):
    if image is not None:
        image_data = await image.read()
        return await upload_image_with_description(image_data, description)
    else:
        return {"message": "Image is missing"}

@router.delete("/delete-image/{image_id}")
async def delete_image_route(image_id: int):
    return await delete_image(image_id)

@router.put("/update-image-description/{image_id}")
async def update_image_description_route(image_id: int, description: str):
    return await update_image_description(image_id, description)

@router.get("/get-image/{image_id}")
async def get_image_route(image_id: int):
    return await get_image_by_id(image_id)
