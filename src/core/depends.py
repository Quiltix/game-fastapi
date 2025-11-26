
from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import authenticate_user
from src.db.session import get_database_session

DatabaseDep = Annotated[AsyncSession, Depends(get_database_session)]
UserDep = Annotated[int, Depends(authenticate_user)]
