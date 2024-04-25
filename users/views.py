from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.validations import get_current_auth_user_for_refresh
from models.user import User
from users.crud import validate_auth_user, get_current_active_auth_user
from users.schemas import UserCreate, UserSchema, UserResponse, TokenInfo
from core.database import get_async_session
from users import crud
from auth.utils import create_access_token, create_refresh_token

router = APIRouter(prefix="/users")


@router.post("/register")
async def create_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    if not user_data.email:
        raise HTTPException(status_code=400, detail="Email is required")
    if not user_data.username:
        raise HTTPException(status_code=400, detail="Username is required")
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters long"
        )

    existing_user = await session.execute(
        select(User).where(User.email == user_data.email)
    )
    if existing_user.scalar():
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )

    return await crud.create_user(user_data, session)


@router.post("/login", response_model=TokenInfo)
async def login_user(
    username: str = Form(..., description="Enter your username"),
    password: str = Form(..., description="Enter your password"),
    session: AsyncSession = Depends(get_async_session),
):
    user = await validate_auth_user(
        session=session,
        username=username,
        password=password,
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return {"access": access_token, "refresh": refresh_token}


@router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
async def auth_refresh_jwt(
    user: UserSchema = Depends(get_current_auth_user_for_refresh),
):
    print(user)
    access_token = create_access_token(user)
    print(access_token)
    return TokenInfo(access=access_token)


# Sample of JWT-protected rout
@router.get("/me", response_model=UserResponse)
async def current_user(
    user: UserSchema = Depends(get_current_active_auth_user),
):
    return {
        "username": user.username,
        "email": user.email,
        "registered_at": user.registered_at,
        "is_verified": user.is_verified,
    }
