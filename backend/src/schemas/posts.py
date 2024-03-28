from pydantic import BaseModel, Field
from datetime import datetime


class PostModel(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=255)
    image: str = Field(min_length=6, max_length=10)


class PostCreate(PostModel):
    post: PostModel
    detail: str = "Post successfully created"


class PostUpdate(PostModel):
    post: PostModel
    detail: str = "Post successfully updated"

class PostDelete(PostModel):
    post: PostModel
    detail: str = "Post successfully deleted"

