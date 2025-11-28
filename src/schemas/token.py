from src.core.schemas import BaseSchema


class TokenData(BaseSchema):
    """Схема данных токена."""

    sub: str
