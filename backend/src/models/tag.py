from src.models.base import CommonBase
from sqlalchemy import Column, String

class Tag(CommonBase):
    __tablename__ = "tags"
    name = Column(String, unique=True, index=True)
