# src/services/user_service.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException, ConflictException

from src.db.models import UserModel
from src.schemas.user import UserCreateSchema


async def get_user_by_username(db: AsyncSession, username: str, raise_if_not_found: bool = True) -> UserModel | None:
    """
    Находит пользователя по имени.

    Args:
        db: Сессия базы данных.
        username: Имя пользователя для поиска.
        raise_if_not_found: Если True, вызывает исключение NotFoundException,
                            если пользователь не найден. Если False, возвращает None.

    Returns:
        Объект UserModel или None.
    """
    query = select(UserModel).where(UserModel.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None and raise_if_not_found:
        raise NotFoundException(detail=f"Пользователь с именем '{username}' не найден.")

    return user


async def create_user(db: AsyncSession, schema: UserCreateSchema) -> UserModel:
    """
    Создает нового пользователя в базе данных.

    Args:
        db: Сессия базы данных.
        schema: Pydantic-схема с данными для создания пользователя.

    Returns:
        Созданный объект UserModel.
    """

    existing_user = await get_user_by_username(db, username=schema.username, raise_if_not_found=False)
    if existing_user:
        raise ConflictException(detail=f"Пользователь с именем '{schema.username}' уже существует.")
    new_user_obj = UserModel(**schema.model_dump())
    db.add(new_user_obj)
    await db.flush()
    await db.refresh(new_user_obj)

    return new_user_obj
