# app/schemas/user.py

from datetime import datetime

from pydantic import EmailStr

from src.core.schemas import BaseSchema


class UserBaseSchema(BaseSchema):
    """Base schema for user data, containing common fields."""

    username: str


class UserCreateSchema(UserBaseSchema):
    """Schema for creating a user, includes the hashed password."""

    hashed_password: str


class UserResponseSchema(UserBaseSchema):
    """Schema for user data in API responses."""

    id: int
    created_at: datetime
    is_active: bool

