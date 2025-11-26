from pydantic import EmailStr

from src.core.schemas import BaseSchema


class RegisterRequestSchema(BaseSchema):
    """Schema for register."""

    username: str
    password: str


class LoginRequestSchema(BaseSchema):
    """Schema for login."""

    username: str
    password: str


class TokenResponseSchema(BaseSchema):
    """Schema for response token."""

    access_token: str
    token_type: str = "bearer"
