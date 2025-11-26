from datetime import datetime, UTC, timedelta

import bcrypt
from jose import jwt

from src.core.config import settings
from src.schemas.token import TokenData


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode("utf-8")


def create_token(data: TokenData) -> str:
    to_encode = data.model_dump()

    expires = datetime.now(UTC) + timedelta(minutes=settings.jwt.access_token_expire_minutes)

    to_encode.update({"exp": expires})

    return jwt.encode(to_encode, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)


def decode_token(token: str) -> TokenData:

    payload = jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])

    return TokenData.model_validate(payload)