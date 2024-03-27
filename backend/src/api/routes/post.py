from fastapi import APIRouter, File, UploadFile, Depends
from src.models import Post, User
from src.schemas.posts import PostCreate, PostModel
from src.crud.post import upload_image_with_description, delete_image, update_image_description, get_image_by_id
from src.services.auth import auth_service

router = APIRouter()


@router.post("/upload-image}", response_model=PostCreate)
async def upload_image_route(body: PostModel, user: User = Depends(auth_service.get_current_user), image: UploadFile = File()):
    image = await upload_image_with_description(user, image, body)
    return {"post": image, "detail": "Post successfully created"}


@router.delete("/delete-image/{image_id}")
async def delete_image_route(image_id: int):
    return await delete_image(image_id)

@router.put("/update-image-description/{image_id}")
async def update_image_description_route(image_id: int, description: str):
    return await update_image_description(image_id, description)


@router.get("/get-image/{image_id}")
async def get_image_route(image_id: int):
    return await get_image_by_id(image_id)
