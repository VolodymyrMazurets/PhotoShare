from libgravatar import Gravatar
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from src.models import User
from src.constants.role import UserRole
from src.schemas.users import UserModel
from src.core.config import settings
from src.core.db import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


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
    return user


async def get_user_by_id(id: int, db: Session, active: bool | None = True) -> User:
    query = db.query(User).filter(
        User.id == id,
    )
    if active is not None:
        query = query.filter(User.active == active)
    return query.first()


async def delete_user(user_id: int, db: Session) -> User:
    user = await get_user_by_id(user_id, active=False, db=db)
    if user:
        db.delete(user)
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