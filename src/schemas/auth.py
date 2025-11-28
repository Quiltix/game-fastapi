from pydantic import EmailStr, Field

from src.core.schemas import BaseSchema


class RegisterRequestSchema(BaseSchema):
    """Схема для регистрации."""

    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=5, max_length=64)


class LoginRequestSchema(BaseSchema):
    """Схема для авторизации."""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=5, max_length=50)


class TokenResponseSchema(BaseSchema):
    """Схема для токена."""

    access_token: str
    token_type: str = "bearer"

class UserUpdateUsernameSchema(BaseSchema):
    """Схема для обновления имени пользователя."""
    new_username: str = Field(..., min_length=3, max_length=50)


class UserUpdatePasswordSchema(BaseSchema):
    """Схема для обновления пароля."""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=50)
