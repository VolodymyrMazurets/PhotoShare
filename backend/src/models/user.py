from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from src.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    username = Column(String(50), unique=True)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    role = Column(String, default="user")
    comments = relationship("Comment", back_populates="user")
    posts = relationship("Post", back_populates="user")