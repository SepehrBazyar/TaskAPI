import ormar
import orjson
from pydantic import (
    Field,
    root_validator,
    BaseModel as PydanticBaseModel,
)
from abc import ABC
from uuid import UUID, uuid4
from typing import Optional, Dict, Any


MOBILE_PATTERN = "^9\\d{9}$"


class BaseModel(PydanticBaseModel):
    """Custom Basic Model Schema to ORM Mode and JSON Encoders"""

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class SuccessfullSchema(BaseModel):
    """Schema of True Boolean Value for Response in Successful Proccess"""

    status: bool = True


class PrimaryKeySchema(BaseModel):
    """Schema of UUID Primary Key Value for Response in Create New Entity"""

    id: UUID


class ItemsPerPage(BaseModel):
    """Class Dependency for get itemsPerPage Params to Paginations"""

    itemsPerPage: int = Field(default=20, ge=1)
    page: int = Field(default=1, ge=0)


class Pagination(BaseModel):
    """Class Model to Pydantic Validation Result Paginations Pages"""

    count: int = Field(default=0, ge=0)
    next: Optional[str] = Field(default=None)
    previous: Optional[str] = Field(default=None)
    results: list = Field(default=[])


class ValidUpdateMixinSchema(BaseModel):
    """Mixin Schema to Root Validator for Check All Fields is not None"""

    @root_validator(pre=True)
    def check_all_not_none(cls, values: Dict[str, Optional[Any]]):
        """Validator to Check All Fields is not None and a Field is Changes"""

        for value in values.values():
            if value is not None:
                return values

        raise ValueError("No Changes were Done.")


class PrimaryKeyMixin:
    """Mixin Class of UUID Primary Key Value for Response in Create New Entity"""

    id: UUID = ormar.UUID(uuid_format="string", primary_key=True, default=uuid4)
