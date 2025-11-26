"""Routes module."""

from .auth import router as auth_router

from .lottery import router as lottery_router
from .users import router as users_router

routers = [auth_router, users_router, file_router, lottery_router]