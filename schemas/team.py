from pydantic import Field
from typing import Optional, List
from core import BaseModel, Pagination, UUIDSchema
from .user import UserBriefSchema


class TeamInDBSchema(BaseModel):
    """Schema to Create New Team with Creator ID as Owner Role"""

    name: str = Field(min_length=3, max_length=64)


class TeamOutDBSchema(BaseModel):
    """Schema to Retrieve Team with Creator Brief Detial Information"""

    name: str = Field(min_length=3, max_length=64)
    creator: UserBriefSchema


class TeamUpdateSchema(BaseModel):
    """Schema for Update Team Fields All is Optional Items Remove Unsets"""

    name: Optional[str] = Field(default=None, min_length=3, max_length=64)


class TeamBriefSchema(UUIDSchema):
    """Schema of the Brief Detials Team to Showing in Teams List"""

    name: str = Field(min_length=3, max_length=64)


class TeamListSchema(Pagination):
    """Schema of Teams List with Pagination Items Count & Next & Previous"""

    results: List[TeamBriefSchema] = Field(default=[])
