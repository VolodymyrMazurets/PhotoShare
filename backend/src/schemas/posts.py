
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from src.schemas.tags import TagResponse


class PostModel(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=255)


class PostModelCreate(PostModel):
    tags: list[str] = []


class PostModelWithImage(PostModel):
    id: int
    created_at: datetime
    image: str = Field(min_length=1, max_length=255)
    tags: List[TagResponse]


class PostCreate(BaseModel):
    post: PostModelWithImage
    detail: str = "Post successfully created"


class PostUpdate(BaseModel):
    post: PostModelWithImage
    detail: str = "Post successfully updated"


class PostDelete(BaseModel):
    post: PostModelWithImage
    detail: str = "Post successfully deleted"
