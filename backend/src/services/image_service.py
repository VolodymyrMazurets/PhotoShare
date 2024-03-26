from src.models.image import Image

async def upload_image_with_description(image_data: bytes, description: str):
    image = Image(data=image_data, description=description)
    await image.save()
    return {"message": "Image uploaded successfully with description"}

async def delete_image(image_id: int):
    image = await Image.get(id=image_id)
    await image.delete()
    return {"message": f"Image with ID {image_id} deleted successfully"}

async def update_image_description(image_id: int, description: str):
    image = await Image.get(id=image_id)
    image.description = description
    await image.save()
    return {"message": f"Description for image with ID {image_id} updated successfully"}

async def get_image_by_id(image_id: int):
    image = await Image.get(id=image_id)
    return {"id": image.id, "data": image.data, "description": image.description}
