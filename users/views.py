from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import User
from users.schemas import UserCreate
from utils.database import get_async_session
from users import crud

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
