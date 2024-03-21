# DB models there
import enum
from sqlalchemy import Column, Integer, String, func, Boolean, Enum
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"


class UserLogin(Base):
    __tablename__ = 'users_login'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    active = Column(Boolean, default=False)
    role = Column(String, default="user")