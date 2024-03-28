from sqlalchemy import Column, String, Boolean
from src.models.base import Base
from sqlalchemy import Column, Integer, func
from sqlalchemy.sql.sqltypes import DateTime

class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('update_at', DateTime, default=func.now())
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    active = Column(Boolean, default=False)
    role = Column(String, default="user")
