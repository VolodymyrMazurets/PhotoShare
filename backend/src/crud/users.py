import redis
import pickle
from libgravatar import Gravatar
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.models.user import User
from src.constants.role import UserRole
from src.schemas.users import UserModel, UserUpdate
from src.core.config import settings
from src.core.db import get_db
from src.constants.messages import AUTH_CANT_FIND_USER, OPERATION_FORBIDDEN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
r = redis.Redis(host=settings.REDIS_HOST_,
                port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, db=0)


async def get_user_by_email(email: str, db: Session) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=AUTH_CANT_FIND_USER)
    return user


async def get_user_by_username(username: str, db: Session) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=AUTH_CANT_FIND_USER)
    return user


async def get_user_by_email_or_username(email: str, username: str, db: Session) -> User:
    user = db.query(User).filter(
        or_(User.email == email, User.username == username)).first()
    return user


async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    if not db.query(User).count():
        roles = [UserRole.admin]
    else:
        roles = [UserRole.user]
    new_user = User(**body.model_dump(), avatar=avatar, role=roles[0])
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    db.refresh(user)
    r.set(f"user:{email}", pickle.dumps(user))
    return user


async def delete_user(user_id: int, db: Session, current_user: User) -> User:
    user = db.query(User).filter(and_(or_(User.id == user_id, current_user.id == User.id),
                                      or_(current_user.role == 'admin', current_user.role == 'moderator'))).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=AUTH_CANT_FIND_USER)
    db.delete(user)
    db.commit()
    return user


async def update_user(user_id: int, body: UserUpdate, db: Session, current_user: User) -> User:
    user = db.query(User).filter(
        and_(User.id == user_id, current_user.id == User.id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=AUTH_CANT_FIND_USER)
    user.email = body.email
    user.username = body.username
    db.commit()
    db.refresh(user)
    return user


async def update_role(user_id: int, role: str, db: Session, current_user: User) -> User:
    if role == 'admin' and current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=OPERATION_FORBIDDEN)
    if role == 'moderator' and current_user.role == 'user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=OPERATION_FORBIDDEN)
    user = db.query(User).filter(
        and_(User.id == user_id, current_user.role == 'admin')).first()
    if user:
        user.role = role
        r.set(f"user:{current_user.email}", pickle.dumps(user))
    db.commit()
    return user


async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, self.SECRET_KEY,
                             algorithms=[self.ALGORITHM])
        if payload['scope'] == 'access_token':
            email = payload["sub"]
            if email is None:
                raise credentials_exception
        else:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    user = await get_user_by_email(email, db)
    if user is None:
        raise credentials_exception
    return user


async def toggle_user_status(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=AUTH_CANT_FIND_USER)
    user.active = not user.active
    db.commit()
    return user
