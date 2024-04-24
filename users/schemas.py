from typing import Annotated

from pydantic import BaseModel, EmailStr
from annotated_types import MinLen, MaxLen


class UserCreate(BaseModel):
    email: EmailStr
    username: Annotated[str, MinLen(5), MaxLen(20)]
    password: str
