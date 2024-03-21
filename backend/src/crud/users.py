from libgravatar import Gravatar
from sqlalchemy.orm import Session

from models import UserLogin, UserRole
from schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> UserLogin:
    return db.query(UserLogin).filter(UserLogin.email == email).first()


async def get_user_by_username(db: Session, username: str) -> UserLogin:
    return db.query(UserLogin).filter(UserLogin.username == username).first()


async def create_user(body: UserModel, db: Session) -> UserLogin:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = UserLogin(**body.model_dump(), avatar=avatar)
    if not db.query(UserLogin).count():
        roles = [UserRole.admin]
    else:
        roles = [UserRole.user]
    new_user = UserLogin(**body.model_dump(), avatar=avatar, role=roles[0])
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    return new_user


async def update_token(user: UserLogin, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> UserLogin:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
