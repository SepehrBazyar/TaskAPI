from pydantic import Field
from typing import Optional, List
from core import BaseModel, Pagination, PrimaryKeySchema
from .user import UserBriefSchema


class TeamNameSchema(BaseModel):
    """Schema to Shared Fields of Team Model Contain Name String"""

    name: str = Field(min_length=3, max_length=64)


class TeamBriefSchema(PrimaryKeySchema, TeamNameSchema):
    """Schema of the Brief Detials Team to Showing in Teams List"""

    pass


class TeamInDBSchema(TeamNameSchema):
    """Schema to Create New Team with Creator ID as Owner Role"""

    pass


class TeamOutDBSchema(TeamNameSchema):
    """Schema to Retrieve Team with Creator Brief Detial Information"""

    creator: UserBriefSchema


class TeamUpdateSchema(BaseModel):
    """Schema for Update Team Fields All is Optional Items Remove Unsets"""

    name: Optional[str] = Field(default=None, min_length=3, max_length=64)


class TeamListSchema(Pagination):
    """Schema of Teams List with Pagination Items Count & Next & Previous"""

    results: List[TeamBriefSchema] = Field(default=[])
