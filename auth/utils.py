# C:\Users\user1\PycharmProjects\FastAPi-actual\auth\utils.py
from datetime import datetime, timedelta

import jwt
from passlib.hash import argon2

from core.config import settings


def encode_jwt(
    payload: dict,
    key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        key,
        algorithm=algorithm,
    )
    return encoded


def decoded_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(password: str) -> str:
    return argon2.hash(password)


def validate_password(password: str, hashed_password: str) -> bool:
    if argon2.verify(password, hashed_password):
        argon2.verify(password, hashed_password)
        return True
    else:
        return False
