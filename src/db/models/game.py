from enum import StrEnum

from sqlalchemy import Enum, String, ForeignKey, DateTime, func
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


class Game(BaseModel):
    __tablename__ = "games"

    status: Mapped[GameStatus] = mapped_column("status",Enum(GameStatus), default=GameStatus.PENDING, nullable=False)

    # Храним состояние доски в виде строки из 9 символов, где '_' - пустая клетка
    # Например: "X_O___O_X"
    board_state: Mapped[str] = mapped_column(String(9), default="""___
                                                                   ___
                                                                   ___""", nullable=False)

    result: Mapped[GameResult] = mapped_column("result",Enum(GameResult),
                                               nullable=True)

    winner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    winner = relationship("User")

    player_associations = relationship("GamePlayer", back_populates="game", cascade="all, delete-orphan")


class PlayerSymbol(StrEnum):
    X = "X"
    O = "O"


class GamePlayer(BaseModel):
    __tablename__ = "game_players"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), primary_key=True)

    symbol: Mapped[PlayerSymbol] = mapped_column("symbol",Enum(PlayerSymbol), nullable=False)

    user = relationship("User", back_populates="game_associations")
    game = relationship("Game", back_populates="player_associations")

