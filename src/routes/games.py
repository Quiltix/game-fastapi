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


@router.post("/", response_model=GameResponseSchema, status_code=status.HTTP_201_CREATED, summary="Создать новую игру")
async def create_new_game(user_id: UserDep, db: DatabaseDep):
    """Создает новую игру, ожидающую второго игрока.

    При создании игры автоматически добавляется создатель игры.

    Необходима авторизация."""
    new_game = await game_service.create_new_game(db=db, user_id=user_id)
    return new_game


@router.post("/{game_id}/join", response_model=GameResponseSchema, summary="Присоединиться к игре")
async def join_game(game_id: int, user_id: UserDep, db: DatabaseDep):
    """Присоединяет текущего пользователя к игре, которая ожидает подключение.

    Если игра уже началась, возвращает ошибку.

    Если игра уже заполнена, возвращает ошибку.

    Если игры нет, возвращает ошибку.

    Возвращает обновленное состояние игры.

    Необходима авторизация."""
    updated_game = await game_service.add_player_to_game(db=db, game_id=game_id, user_id=user_id)
    return updated_game

@router.post("/{game_id}/move", response_model=GameResponseSchema, summary="Совершить ход в игре")
async def make_move(
        game_id: int,
        move: MakeMoveRequestSchema,  # Принимаем позицию в теле запроса
        user_id: UserDep,
        db: DatabaseDep
):
    """
    Совершает ход в активной игре.

    Принимает идентификатор игры и позицию(0-8).

    Если ход успешен, игра обновляется.

    Если ход не удался, возвращается ошибка.

    Возвращает обновленное состояние игры.

    Необходима авторизация.
    """
    updated_game = await game_service.process_player_move(
        db=db,
        game_id=game_id,
        user_id=user_id,
        position=move.position
    )
    return updated_game


@router.get("/active", response_model=list[GameResponseSchema], summary="Получить список доступных игр")
async def get_available_games(db: DatabaseDep, user_id: UserDep):
    """Возвращает список игр, ожидающих второго игрока.

    Необходима авторизация.
    """
    return await game_service.get_available_games(db=db)

@router.get("/{game_id}", response_model=GameResponseSchema, summary="Получить детали игры")
async def get_game_details(game_id: int, db: DatabaseDep, user_id: UserDep):
    """Возвращает детальную информацию о конкретной игре.

    Принимает id игры.

    Необходима авторизация."""
    game = await game_service.get_game_by_id(db=db, game_id=game_id)
    return game

@router.get("/", response_model=list[GameResponseSchema], summary="Получить все завершенные игры")
async def get_game_details(db: DatabaseDep, user_id: UserDep):
    """Возвращает детальную информацию о завершенных играх.

    Необходима авторизация."""
    return await game_service.get_all_completed_games(db=db)