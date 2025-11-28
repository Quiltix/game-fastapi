# app/schemas/user.py



from src.core.schemas import BaseSchema


class UserBaseSchema(BaseSchema):
    """Базовая схема пользователя."""
    username: str


class UserCreateSchema(UserBaseSchema):
    """Схема для создания нового пользователя."""

    hashed_password: str


class UserResponseSchema(UserBaseSchema):
    """Схема для ответа на запрос пользователя."""

    id: int
    username: str
    is_active: bool

