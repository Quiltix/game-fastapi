"""Base model for database models."""

from typing import Any, TypeVar

from sqlalchemy.orm import DeclarativeBase, declared_attr

_T = TypeVar("_T", bound="BaseModel")


class BaseModel(DeclarativeBase):
    """Base model for SQLAlchemy ORM."""

    __abstract__ = True

    def __repr__(self) -> str:
        """
        Возвращает удобное для отладки представление объекта.
        Пример: <User id=1>
        """
        pk_name = self.__table__.primary_key.columns.keys()[0]
        pk_value = getattr(self, pk_name, None)
        return f"<{self.__class__.__name__} {pk_name}={pk_value}>"

    def to_dict(self) -> dict[str, Any]:
        """
        Преобразует объект модели в словарь.
        Безопасный способ, который включает только колонки таблицы.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}