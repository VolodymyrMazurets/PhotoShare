from fastapi import APIRouter, HTTPException, Depends, status
from src.core.db import get_db
from src.models import User
from src.schemas.users import UserResponseProfile, UserUpdate, UserDb
from src.crud import users as repository_users
from sqlalchemy.orm import Session
from src.services.auth import auth_service


router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/me", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user

@router.get('/{username}', response_model=UserResponseProfile)
async def user_info(username: str, db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {'user': user}



@router.delete('/delete_user', response_model=UserResponseProfile)
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.delete_user(user_id, db, current_user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {'user': user}


@router.put('/{user_id}', response_model=UserResponseProfile)
async def update_user(user_id: int, body: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.update_user(user_id, body, db, current_user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {'user': user}


@router.patch('/update_role', response_model=UserResponseProfile)
async def update_role(user_id: int, role: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.update_role(user_id, role, db, current_user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {'user': user}