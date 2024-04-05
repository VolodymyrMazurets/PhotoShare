from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base_model import BaseModel

class Comment(BaseModel):
    __tablename__ = "comments"
    content = Column(String)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), default=None)
    post_id = Column(Integer, ForeignKey(
        'posts.id', ondelete='CASCADE'), default=None)
    user = relationship("User", back_populates="comments",)
    post = relationship("Post", back_populates="comments",)