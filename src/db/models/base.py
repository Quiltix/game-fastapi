"""Base model for database models."""

from typing import Any, TypeVar

from sqlalchemy.orm import DeclarativeBase

from app.lib.schemas.base import BaseSchema

_T = TypeVar("_T", bound="BaseModel")


class BaseModel(DeclarativeBase):
    """Base model for SQLAlchemy ORM."""

    __abstract__ = True

    def __repr__(self) -> str:
        """Return the representation of the model."""
        _repr = f"<{self.__class__.__name__} "
        for name in self._get_primary_keys():
            _repr += f"{name}={self._get_key_value(name)}, "
        return _repr[:-2] + ">"

    def __str__(self) -> str:
        """Return the string representation of the model."""
        return self.__repr__()

    def to_dict(self) -> dict[str, Any]:
        """Return the dictionary representation of the model."""
        return self.__dict__

    @classmethod
    def from_dict(cls: type[_T], data: dict[str, Any]) -> _T:
        """Create a model from a dictionary."""
        return cls(**data)

    @classmethod
    def from_schema(cls: type[_T], model: BaseSchema) -> _T:
        """Create a model from pydantic schema."""
        return cls.from_dict(model.model_dump())

    @classmethod
    def _get_primary_keys(cls) -> list[str]:
        """Return the primary keys of the model."""
        return [i.name for i in cls.__table__.primary_key.columns.values()]  # type: ignore[attr-defined]

    def _get_key_value(self, name: str) -> Any:
        """Return the primary key value of the model."""
        return getattr(self, name)
