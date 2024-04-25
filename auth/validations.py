from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import decode_jwt
from core.database import get_async_session
from models import User
from users.schemas import UserSchema

http_bearer = HTTPBearer()


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> UserSchema:
    token = credentials.credentials
    try:
        payload = decode_jwt(token=token)
        return payload
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}"
        )


def validate_token_type(payload: dict, token_type: str) -> bool:
    if payload.get("type") == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
    )


async def get_user_by_token_sub(
    payload: dict, session: AsyncSession = Depends(get_async_session)
) -> UserSchema:
    user_id: int | None = payload.get("sub")
    result = await session.execute(select(User).filter(User.id == user_id))
    (user,) = result.fetchone()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(get_async_session),
    ):
        validate_token_type(payload, self.token_type)
        return await get_user_by_token_sub(payload=payload, session=session)


get_current_auth_user = UserGetterFromToken("access")
get_current_auth_user_for_refresh = UserGetterFromToken("refresh")
