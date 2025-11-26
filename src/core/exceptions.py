from fastapi import status
from fastapi import Request
from fastapi.responses import JSONResponse
from traceback import print_exception

async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, BaseAppException):
        exception_content = {"detail": exc.detail, "additional_info": exc.additional_info}
        print_exception(exc)
        return JSONResponse(status_code=exc.status_code, content=exception_content)

    raise exc
class BaseAppException(Exception):
    """
    Базовый класс для всех кастомных исключений в приложении.
    """
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Произошла непредвиденная ошибка на сервере."

    def __init__(self, detail: str | None = None, status_code: int | None = None):
        if detail is not None:
            self.detail = detail
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.detail)

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
