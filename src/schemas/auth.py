from pydantic import EmailStr

from src.core.schemas import BaseSchema


class RegisterRequestSchema(BaseSchema):
    """Схема для регистрации."""

    username: str
    password: str


class LoginRequestSchema(BaseSchema):
    """Схема для авторизации."""

    username: str
    password: str


class TokenResponseSchema(BaseSchema):
    """Схема для токена."""

    access_token: str
    token_type: str = "bearer"
