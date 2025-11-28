from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Базовая схема для всех схем."""

    class Config:
        """Конфигурация схемы."""

        from_attributes = True # Преобразование атрибутов в объекты
        validate_by_name = True # Проверка по имени
        use_enum_values = True # Использование значений enum
        str_strip_whitespace = True # Удаление пробелов в начале и конце строки