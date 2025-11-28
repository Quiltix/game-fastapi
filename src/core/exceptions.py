from typing import Any

from fastapi import status
from fastapi import Request
from fastapi.responses import JSONResponse
from traceback import print_exception

async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Перехватывает все исключения и возвращает JSON-ответ с деталями ошибки."""
    if isinstance(exc, BaseAppException):
        exception_content = {"detail": exc.detail, "additional_info": exc.additional_info}
        print_exception(exc)
        return JSONResponse(status_code=exc.status_code, content=exception_content)

    raise exc

class BaseAppException(Exception):
    """Базовое исключение для приложения."""

    detail: str = "An application error occurred."
    status_code: int = 500
    additional_info: dict[str, Any] = {}

    def __init__(
        self,
        *args: Any,
        detail: str | None = None,
        status_code: int | None = None,
        additional_info: dict[str, Any] = {},
    ) -> None:
        """Init base exception."""
        self.detail = detail if detail is not None else self.__class__.detail
        self.status_code = status_code if status_code is not None else self.__class__.status_code
        self.additional_info = additional_info

        super().__init__(*(str(arg) for arg in args if arg))

    def __str__(self) -> str:
        return self.detail

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(detail={self.detail!r}, status_code={self.status_code},"
            f"additional_info: {self.additional_info})"
        )

class NotFoundException(BaseAppException):
    """
    Исключение, вызываемое при попытке доступа к несуществующему ресурсу.
    """
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "Запрашиваемый ресурс не найден."

class BadRequestException(BaseAppException):
    """
    Исключение, вызываемое при некорректном запросе клиента.
    """
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Некорректный запрос."
class UnauthorizedException(BaseAppException):
    """
    Исключение, вызываемое при попытке доступа без авторизации.
    """
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Требуется авторизация для доступа к ресурсу."

class InvalidCredentialsException(UnauthorizedException):
    """
    Исключение, вызываемое при предоставлении неверных учетных данных.
    """
    detail: str = "Неверные учетные данные."

class ConflictException(BaseAppException):
    """
    Исключение, вызываемое при конфликте состояний.
    """
    status_code: int = status.HTTP_409_CONFLICT
    detail: str = "Конфликт состояний."

class ForbiddenException(BaseAppException):
    """
    Исключение, вызываемое при попытке доступа к ресурсу с недостаточными правами.
    """
    status_code: int = status.HTTP_403_FORBIDDEN
    detail: str = "Доступ запрещен."



