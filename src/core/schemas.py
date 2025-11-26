from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Base schema for Pydantic models."""

    class Config:
        """Configuration for Pydantic models."""

        from_attributes = True
        validate_by_name = True
        use_enum_values = True
        str_strip_whitespace = True