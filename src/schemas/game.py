from datetime import datetime
from pydantic import ConfigDict

from src.core.schemas import BaseSchema
from src.db.models.game import GameStatus, GameResult, PlayerSymbol
from src.schemas.user import UserResponseSchema


class PlayerInGameSchema(BaseSchema):
    """
    Представляет одного игрока внутри игровой сессии.
    """
    symbol: PlayerSymbol
    user: UserResponseSchema

    model_config = ConfigDict(from_attributes=True)



class GameResponseSchema(BaseSchema):

    id: int
    status: GameStatus
    board_state: str
    result: GameResult | None = None
    created_at: datetime
    finished_at: datetime | None = None

    winner: UserResponseSchema | None = None
    players: list[PlayerInGameSchema]

    model_config = ConfigDict(from_attributes=True)