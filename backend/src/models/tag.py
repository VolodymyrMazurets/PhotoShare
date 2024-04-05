
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.models.base_model import BaseModel
from src.models.helpers import post_m2m_tag

class Tag(BaseModel):
    __tablename__ = "tags"
    name = Column(String, unique=True, index=True)
    posts = relationship("Post", secondary=post_m2m_tag, back_populates="tags")