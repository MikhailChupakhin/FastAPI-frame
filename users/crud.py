from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from users.schemas import UserCreate
from passlib.hash import argon2


async def create_user(user_data: UserCreate, session: AsyncSession):
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=argon2.hash(user_data.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"message": f"User {new_user.username} created successfull"}
