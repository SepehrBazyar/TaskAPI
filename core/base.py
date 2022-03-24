import orjson
from pydantic import (
    Field,
    BaseModel as PydanticBaseModel,
)
from uuid import UUID
from typing import Optional


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


class UUIDSchema(BaseModel):
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
