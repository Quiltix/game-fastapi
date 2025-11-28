"""Base model for database models."""

from typing import Any, TypeVar

from sqlalchemy.orm import DeclarativeBase, declared_attr

_T = TypeVar("_T", bound="BaseModel")


class BaseModel(DeclarativeBase):
    """Base model for SQLAlchemy ORM."""

    __abstract__ = True