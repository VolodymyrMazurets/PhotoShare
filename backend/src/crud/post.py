from src.crud.post import Image
import cloudinary.uploader

cloudinary.config(
    cloud_name= "CLOUD_NAME",
    api_key= "API_KEY",
    api_secret= "API_SECRET"
)

async def upload_image_with_description(image_data: bytes, description: str):
    try:
        upload_result = cloudinary.uploader.upload(image_data)
        image_url = upload_result['secure_url']
        image = Image(url=image_url, description=description)
        await image.save()
        return {"message": "Image uploaded successfully with description"}
    except Exception as e:
        return {"message": f"Failed to upload image: {str(e)}"}

async def delete_image(image_id: int):
    try:
        image = await Image.get(id=image_id)
        deletion_result = cloudinary.uploader.destroy(image.url)
        await image.delete()
        return {"message": f"Image with ID {image_id} deleted successfully"}
    except Exception as e:
        return {"message": f"Failed to delete image: {str(e)}"}


async def update_image_description(image_id: int, description: str):
    try:
        image = await Image.get(id=image_id)
        image.description = description
        await image.save()
        return {"message": f"Description for image with ID {image_id} updated successfully"}
    except Exception as e:
        return {"message": f"Failed to update image description: {str(e)}"}

async def get_image_by_id(image_id: int):
    try:
        image = await Image.get(id=image_id)
        return {"id": image.id, "url": image.url, "description": image.description}
    except Exception as e:
        return {"message": f"Failed to get image by ID: {str(e)}"}

