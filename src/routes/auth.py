from fastapi import APIRouter, status

from src.core.depends import DatabaseDep
from src.schemas.auth import RegisterRequestSchema, TokenResponseSchema, LoginRequestSchema
from src.schemas.user import UserResponseSchema

import src.services.auth as auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema, summary="Регистрация нового пользователя")
async def register(db: DatabaseDep, schema: RegisterRequestSchema) -> UserResponseSchema:
    """Register new user."""
    user = await auth_service.register_new_user(db, schema)
    return UserResponseSchema.model_validate(user)


@router.post("/login", response_model=TokenResponseSchema,summary="Авторизация пользователя")
async def login(db: DatabaseDep, schema: LoginRequestSchema) -> TokenResponseSchema:
    """Login user and generate tokens."""
    user = await auth_service.authenticate_user(db, schema)
    return await auth_service.create_user_tokens(user.id)
