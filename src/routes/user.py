from fastapi import APIRouter, status

from src.core.depends import DatabaseDep, UserDep
from src.schemas.game import GameResponseSchema
from src.schemas.user import UserResponseSchema
from src.services import game as game_service

import src.services.user as user_service

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponseSchema, summary="Получить информацию о текущем пользователе")
async def register(db: DatabaseDep, user_id: UserDep) -> UserResponseSchema:
    """Возвращает информацию о текущем пользователе.

    Необходима авторизация."""
    user = await user_service.get_user_by_id(db, user_id)
    return UserResponseSchema.model_validate(user)


@router.get("/games", response_model=list[GameResponseSchema], summary="Получить историю игр текущего пользователя")
async def get_my_game_history(user_id: UserDep, db: DatabaseDep):
    """Возвращает историю игр текущего пользователя.

    Необходима авторизация."""
    return await game_service.get_user_game_history(db=db, user_id=user_id)