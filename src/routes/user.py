from fastapi import APIRouter, status

from src.core.depends import DatabaseDep, UserDep
from src.schemas.user import UserResponseSchema

import src.services.user as user_service

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def register(db: DatabaseDep, user_id: UserDep) -> UserResponseSchema:
    """Register new user."""
    user = await user_service.get_user_by_id(db, user_id)
    return UserResponseSchema.model_validate(user)


