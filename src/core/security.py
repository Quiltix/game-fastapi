from datetime import datetime, UTC, timedelta

import bcrypt
from fastapi import Depends
from fastapi.security import HTTPBearer
from jose import jwt, JWTError

from src.core.config import settings
from src.core.exceptions import UnauthorizedException
from src.schemas.token import TokenData

async def authenticate_user(credentials: HTTPBearer = Depends(HTTPBearer(auto_error=False))) -> int:
    """Зависимость для аутентификации пользователя."""
    try:
        if not credentials:
            raise JWTError
        token_data = decode_token(credentials.credentials)
        return int(token_data.sub)
    except JWTError:
        raise UnauthorizedException()

def decode_token(token: str) -> TokenData:
    """Декодирует токен и возвращает данные токена."""

    payload = jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])

    return TokenData.model_validate(payload)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    """Возвращает хэш пароля."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode("utf-8")


def create_token(data: TokenData) -> str:
    """Создает токен."""
    to_encode = data.model_dump()

    expires = datetime.now(UTC) + timedelta(minutes=settings.jwt.access_token_expire_minutes)

    to_encode.update({"exp": expires})

    return jwt.encode(to_encode, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)


def decode_token(token: str) -> TokenData:
    """Декодирует токен и возвращает данные токена."""

    payload = jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])

    return TokenData.model_validate(payload)