from src.core.schemas import BaseSchema


class TokenData(BaseSchema):
    """Schema for token data."""

    sub: str
