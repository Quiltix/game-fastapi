# src/services/user_service.py

from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException, ConflictException, ForbiddenException
from src.core.security import verify_password, get_password_hash

from src.db.models import UserModel, Game
from src.db.models.game import GameResult, GamePlayer, GameStatus
from src.schemas.user import UserCreateSchema, UserStatsSchema


async def get_user_by_username(db: AsyncSession, username: str, raise_if_not_found: bool = True) -> UserModel | None:
    """
    Находит пользователя по имени.

    """
    query = select(UserModel).where(UserModel.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None and raise_if_not_found:
        raise NotFoundException(detail=f"Пользователь с именем '{username}' не найден.")

    return user

async def get_user_by_id(db: AsyncSession, id: int, raise_if_not_found: bool = True) -> UserModel | None:
    """Находит пользователя по id."""
    query = select(UserModel).where(UserModel.id == id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None and raise_if_not_found:
        raise NotFoundException(detail="Пользователь не найден.")

    return user


async def create_user(db: AsyncSession, schema: UserCreateSchema) -> UserModel:
    """Создает нового пользователя в базе данных."""

    existing_user = await get_user_by_username(db, username=schema.username, raise_if_not_found=False)
    if existing_user:
        raise ConflictException(detail=f"Пользователь с именем '{schema.username}' уже существует.")
    new_user_obj = UserModel(**schema.model_dump())
    db.add(new_user_obj)
    await db.flush()
    await db.refresh(new_user_obj)

    return new_user_obj


async def update_username(db: AsyncSession, user_id: int, new_username: str) -> UserModel:
    """Обновляет имя пользователя."""
    existing_user = await get_user_by_username(db, new_username, raise_if_not_found=False)
    if existing_user and existing_user.id != user_id:
        raise ConflictException(detail="Имя пользователя уже занято.")
    elif existing_user and existing_user.username == new_username:
        raise ConflictException(detail="Укажите новое имя.")

    user_to_update = await get_user_by_id(db, user_id)
    user_to_update.username = new_username

    await db.flush()
    await db.refresh(user_to_update)
    return user_to_update


async def update_password(db: AsyncSession, user_id: int, current_password: str, new_password: str) -> None:
    user = await get_user_by_id(db, user_id)

    if not verify_password(current_password, user.hashed_password):
        raise ForbiddenException(detail="Неверный текущий пароль.")

    if verify_password(new_password, user.hashed_password):
        raise ConflictException(detail="Новый пароль не может совпадать с текущим.")

    user.hashed_password = get_password_hash(new_password)

    await db.flush()


async def delete_user(db: AsyncSession, user_id: int) -> UserModel:
    """
    Выполняетудаление пользователя.

    - Устанавливает is_active = False.
    - Изменяет username на 'deleted_user_id'.
    """
    user_to_delete = await get_user_by_id(db, user_id)
    user_to_delete.is_active = False

    user_to_delete.username = f"deleted_user_{user_id}"

    await db.flush()
    await db.refresh(user_to_delete)

    return user_to_delete


async def get_user_stats(db: AsyncSession, user_id: int) -> UserStatsSchema:
    """
    Рассчитывает и возвращает игровую статистику для пользователя.
    """
    # 1. Создаем запрос для агрегации данных
    # Мы хотим посчитать количество побед, поражений и ничьих
    query = (
        select(
            func.count(Game.id).label("total_games"),

            func.sum(case((Game.winner_id == user_id, 1), else_=0)).label("wins"),

            func.sum(case((
                (Game.winner_id != None) & (Game.winner_id != user_id), 1),
                else_=0
            )).label("losses"),

            func.sum(case((Game.result == GameResult.DRAW, 1), else_=0)).label("draws")
        )
        .join(Game.player_associations)
        .where(
            GamePlayer.user_id == user_id,
            Game.status == GameStatus.COMPLETED
        )
    )

    result = await db.execute(query)
    stats_row = result.one()

    wins = stats_row.wins
    losses = stats_row.losses

    if (wins + losses) == 0:
        win_rate = 0.0
    else:
        win_rate = round((wins / (wins + losses)) * 100, 2)

    return UserStatsSchema(
        total_games=stats_row.total_games,
        wins=wins,
        losses=losses,
        draws=stats_row.draws,
        win_rate=win_rate
    )
