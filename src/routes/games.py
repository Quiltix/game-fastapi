from fastapi import APIRouter, status

from src.core.depends import UserDep, DatabaseDep
import src.services.game as game_service
import src.services.user as user_service
from src.schemas.game import GameResponseSchema, MakeMoveRequestSchema
from src.schemas.user import UserResponseSchema

router = APIRouter(
    prefix="/games",
    tags=["Games"],
)


@router.post("/", response_model=GameResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_new_game(user_id: UserDep, db: DatabaseDep):
    """Создает новую игру, ожидающую второго игрока."""
    new_game = await game_service.create_new_game(db=db, user_id=user_id)
    return new_game


@router.post("/{game_id}/join", response_model=GameResponseSchema)
async def join_game(game_id: int, user_id: UserDep, db: DatabaseDep):
    """Присоединяет текущего пользователя к игре."""
    updated_game = await game_service.add_player_to_game(db=db, game_id=game_id, user_id=user_id)
    return updated_game


# --- НОВЫЙ ЭНДПОИНТ ДЛЯ ИГРОВОГО ПРОЦЕССА ---

@router.post("/{game_id}/move", response_model=GameResponseSchema)
async def make_move(
        game_id: int,
        move: MakeMoveRequestSchema,  # Принимаем позицию в теле запроса
        user_id: UserDep,
        db: DatabaseDep
):
    """
    Совершает ход в активной игре.

    Клиент должен передать в теле запроса позицию для хода (0-8).
    В ответ возвращается обновленное состояние игры.
    """
    updated_game = await game_service.process_player_move(
        db=db,
        game_id=game_id,
        user_id=user_id,
        position=move.position
    )
    return updated_game


@router.get("/", response_model=list[GameResponseSchema])
async def get_available_games(db: DatabaseDep, user_id: UserDep):
    """Возвращает список игр, ожидающих второго игрока."""
    return await game_service.get_available_games(db=db)


@router.get("/history", response_model=list[GameResponseSchema])
async def get_my_game_history(user_id: UserDep, db: DatabaseDep):
    """Возвращает историю игр текущего пользователя."""
    return await game_service.get_user_game_history(db=db, user_id=user_id)


@router.get("/{game_id}", response_model=GameResponseSchema)
async def get_game_details(game_id: int, db: DatabaseDep, user_id: UserDep):
    """
    Возвращает детальную информацию о конкретной игре.
    КЛЮЧЕВОЙ ЭНДПОИНТ ДЛЯ ПОЛЛИНГА.
    """
    game = await game_service.get_game_by_id(db=db, game_id=game_id)
    return game