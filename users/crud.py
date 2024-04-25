# C:\Users\user1\PycharmProjects\FastAPi-actual\users\crud.py

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.validations import get_current_auth_user
from auth.utils import hash_password, validate_password
from models.user import User
from users.schemas import UserCreate, UserSchema


async def create_user(user_data: UserCreate, session: AsyncSession):
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"message": f"User {new_user.username} created successfull"}


async def validate_auth_user(
    session: AsyncSession,
    username: str,
    password: str,
):
    result = await session.execute(select(User).filter(User.username == username))
    (user,) = result.fetchone()
    if not user or not validate_password(password, user.hashed_password):
        return None
    return user


def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.is_active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user inactive")
