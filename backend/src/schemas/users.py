from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str
    role : str
    
    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class UserResponseProfile(BaseModel):
    user: UserDb
    detail: str = "Info about user"
    image_count: int = 0


class UserUpdate(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
