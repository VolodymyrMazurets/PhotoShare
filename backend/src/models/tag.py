from src.models.base import Base
from sqlalchemy import Column, String

class Tag(Base):
    __tablename__ = "tags"
    name = Column(String, unique=True, index=True)
