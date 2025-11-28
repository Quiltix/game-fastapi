from enum import StrEnum

from sqlalchemy import Enum, String, ForeignKey, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models import BaseModel


class GameStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
class GameResult(StrEnum):
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    DRAW = "draw"

class PlayerSymbol(StrEnum):
    X = "X"
    O = "O"


class Game(BaseModel):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column("id", Integer(), primary_key=True, autoincrement=True)

    status: Mapped[GameStatus] = mapped_column("status",Enum(GameStatus), default=GameStatus.PENDING, nullable=False)

    board_state: Mapped[str] = mapped_column(String(9), default="_________", nullable=False)

    result: Mapped[GameResult] = mapped_column("result",Enum(GameResult),
                                               nullable=True)

    winner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    winner = relationship("UserModel")

    player_associations = relationship("GamePlayer", back_populates="game", cascade="all, delete-orphan")


class GamePlayer(BaseModel):
    __tablename__ = "game_players"

    id: Mapped[int] = mapped_column("id", Integer(), primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), primary_key=True)

    symbol: Mapped[PlayerSymbol] = mapped_column("symbol",Enum(PlayerSymbol), nullable=False)

    user = relationship("UserModel", back_populates="game_associations")
    game = relationship("Game", back_populates="player_associations")

