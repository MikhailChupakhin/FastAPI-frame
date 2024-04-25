from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr
from annotated_types import MinLen, MaxLen


class TokenInfo(BaseModel):
    access: str
    refresh: str | None = None
    token_type: str = "Bearer"


class UserCreate(BaseModel):
    email: EmailStr
    username: Annotated[str, MinLen(5), MaxLen(20)]
    password: str


class UserSchema(BaseModel):
    id: int
    email: str
    username: str
    registered_at: datetime
    role_id: int
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    username: str
    email: str
    registered_at: datetime
    is_verified: bool
