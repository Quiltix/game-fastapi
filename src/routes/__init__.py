"""Routes module."""

from .auth import router as auth_router
from .user import router as user_router
from .games import router as games_router


routers = [auth_router,user_router,games_router]