from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from src.core.db import get_db
from src.models.user import User
from src.schemas.users import UserUpdate, UserDb
from sqlalchemy.orm import Session
from src.services.auth import auth_service
from src.crud import users as repository_users

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me", response_model=UserDb, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.get('/{username}', response_model=UserDb, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def user_info(username: str, db: Session = Depends(get_db)):
    return await repository_users.get_user_by_username(username, db)


@router.delete('/{user_id}', response_model=UserDb, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    return await repository_users.delete_user(user_id, db, current_user)


@router.patch('/{user_id}', response_model=UserDb, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_user(user_id: int, body: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    return await repository_users.update_user(user_id, body, db, current_user)


@router.patch('/', response_model=UserDb, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_role(user_id: int, role: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    return await repository_users.update_role(user_id, role, db, current_user)
