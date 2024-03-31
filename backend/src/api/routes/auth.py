from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from src.services.email import send_email
from src.core.db import get_db
from src.schemas.users import UserModel, UserResponse
from src.schemas.token import TokenModel
from src.schemas.email import RequestEmail
from src.crud import users as repository_users
from src.services.auth import auth_service
from src.models import User
from src.constants.role import UserRole
from src.core.config import settings
from src.constants.messages import AUTH_EMAIL_NOT_CONF, AUTH_ALREADY_EXIST, AUTH_INVALID_REF_TOKEN, AUTH_CANT_FIND_USER, AUTH_INVALID_PASSWORD, AUTH_BANNED
from src.core.security import  allowed_operation_admin

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    exist_user = await repository_users.get_user_by_email_or_username(body.email, body.username, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=AUTH_ALREADY_EXIST)
    roles = [UserRole.admin] if not db.query(User).count() else [UserRole.user]
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(
        send_email, new_user.email, new_user.username, settings.FRONTEND_URL)
    return {"user": new_user, "role": roles, "detail": "User successfully created. Check your email for confirmation."}


@router.post("/login", response_model=TokenModel, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(body)
    user = await repository_users.get_user_by_username(body.username, db)
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=AUTH_BANNED)
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=AUTH_EMAIL_NOT_CONF)
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=AUTH_INVALID_PASSWORD)
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email, "role": user.role})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=AUTH_INVALID_REF_TOKEN)

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=AUTH_CANT_FIND_USER)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(
            send_email, user.email, user.username, settings.FRONTEND_URL)
    return {"message": "Check your email for confirmation."}


@router.post("/toggle_user_status/{user_id}", dependencies=[Depends(allowed_operation_admin), Depends(RateLimiter(times=10, seconds=60))])
async def toggle_user_status(user_id: int, db: Session = Depends(get_db)):
    user = await repository_users.toggle_user_status(user_id, db)
    if user.active:
        return {"message": "User has been unbanned"}
    return {"message": "User has been banned"}
