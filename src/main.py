"""FastAPI app for navigation service."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.exceptions import BaseAppException, exception_handler

from src.routes import routers

app = FastAPI(title="hack-final", root_path=settings.general.api_prefix, redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.general.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(BaseAppException, exception_handler)

for router in routers:
    app.include_router(router)
