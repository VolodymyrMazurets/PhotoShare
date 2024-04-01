from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CommentModel(BaseModel):
    content: str = Field(max_length=100)
    post_id: int = Field(ge=1)


class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class CommentUpdate(BaseModel):
    new_comment: str = Field(max_length=100)

class CommentBase(BaseModel):
    comment: str = Field(min_length=1, max_length=255)