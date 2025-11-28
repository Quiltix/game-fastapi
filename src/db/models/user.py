from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models import BaseModel


class UserModel(BaseModel):
    """Модель пользователя."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column("id", Integer(), primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    game_associations = relationship("GamePlayer", back_populates="user")