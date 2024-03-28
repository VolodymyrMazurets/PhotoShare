from pydantic import BaseModel, Field
from datetime import datetime


class PostModel(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=255)


class PostModelWithImage(PostModel):
    image: str = Field(min_length=1, max_length=255)
    id: int
    created_at: datetime


class PostCreate(BaseModel):
    post: PostModelWithImage
    detail: str = "Post successfully created"

class PostUpdate(BaseModel):
    post: PostModelWithImage
    detail: str = "Post successfully updated"

class PostDelete(BaseModel):
    post: PostModelWithImage
    detail: str = "Post successfully deleted"

