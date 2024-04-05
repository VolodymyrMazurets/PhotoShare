from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base_model import BaseModel
from src.models.helpers import post_m2m_tag, post_o2m_comment


class Post(BaseModel):
    __tablename__ = "posts"
    title = Column(String, index=True)
    description = Column(String(255))
    image = Column(String(255))
    image_public_id = Column(String(255))
    transformed_image = Column(String(255), default=None)
    transformed_image_qr = Column(String(255), default=None)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), default=None)
    user = relationship("User", back_populates="posts")
    tags = relationship("Tag", secondary=post_m2m_tag, back_populates="posts")
    comments = relationship(
        "Comment", secondary=post_o2m_comment, back_populates="post")
