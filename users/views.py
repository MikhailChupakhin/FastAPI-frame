from fastapi import APIRouter, Depends, HTTPException, Form

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from users.crud import validate_auth_user
from users.schemas import UserCreate
from core.database import get_async_session
from users import crud
from auth.utils import encode_jwt

router = APIRouter(prefix="/users")


@router.post("/login")
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
    jwt_payload = {"sub": user.username}
    token = encode_jwt(jwt_payload)
    return {"access_token": token, "token_type": "Bearer"}


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
