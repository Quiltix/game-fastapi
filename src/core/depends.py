
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.exceptions import UnauthorizedException
from src.db.session import get_database_session


async def authenticate_user(credentials: HTTPBearer = Depends(HTTPBearer(auto_error=False))) -> int:
    """Dependency to authenticate a user."""
    try:
        if not credentials:
            raise JWTError
        token_data = decode_token(credentials.credentials)
        return int(token_data.sub)
    except JWTError:
        raise UnauthorizedException()

def decode_token(token: str) -> TokenData:

    payload = jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])

    return TokenData.model_validate(payload)
# Dependencies for external use
DatabaseDep = Annotated[AsyncSession, Depends(get_database_session)]
UserDep = Annotated[int, Depends(authenticate_user)]
