from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import InvalidCredentialsException
from src.core.security import create_token, get_password_hash, verify_password
from src.db.models import UserModel
from src.schemas.auth import TokenResponseSchema, RegisterRequestSchema, LoginRequestSchema
from src.schemas.token import TokenData
from src.schemas.user import UserCreateSchema

import src.services.user as user_service

async def create_user_tokens(user_id: int) -> TokenResponseSchema:
    """Создает токены для пользователя."""

    _user_id = str(user_id)
    access_token_data = TokenData(sub=_user_id)

    access_token = create_token(access_token_data)

    return TokenResponseSchema(access_token=access_token)


async def register_new_user(db: AsyncSession, schema: RegisterRequestSchema) -> UserModel:
    """Регистрирует нового пользователя."""

    hashed_password = get_password_hash(schema.password)

    create_schema = UserCreateSchema(
        username=schema.username,
        hashed_password=hashed_password,
    )

    user = await user_service.create_user(db, create_schema)
    return user


async def authenticate_user(db: AsyncSession, schema: LoginRequestSchema) -> UserModel:
    """Аутентифицирует пользователя."""

    user = await user_service.get_user_by_username(db=db, username=schema.username, raise_if_not_found=False)

    if not user or not verify_password(schema.password, user.hashed_password):
        raise InvalidCredentialsException()

    return user
