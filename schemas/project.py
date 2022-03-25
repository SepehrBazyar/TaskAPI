from pydantic import Field
from uuid import UUID
from datetime import date
from typing import Optional, List
from core import BaseModel, Pagination, UUIDSchema
from .team import TeamBriefSchema


class ProjectBriefSchema(UUIDSchema):
    """Schema of Brief Detials Project to Showing in Projects List with Team Info"""

    name: str
    team: TeamBriefSchema


class OptionalFieldSchema(BaseModel):
    """Schema to Shared Fields of Project Model is Optional Can be None"""

    description: Optional[str] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)


class ProjectInDBSchema(OptionalFieldSchema):
    """Schema to Create New Team with Creator ID as Owner Role"""

    name: str = Field(min_length=3, max_length=64)
    team_id: UUID


class ProjectOutDBSchema(ProjectBriefSchema, OptionalFieldSchema):
    """Schema to Retriever Team with Creator ID as Owner Role"""

    pass


class ProjectUpdateSchema(OptionalFieldSchema):
    """Schema for Update Project Fields All is Optional Items Remove Unsets"""

    name: Optional[str] = Field(default=None, min_length=3, max_length=64)
    team_id: Optional[UUID] = Field(default=None)


class ProjectListSchema(Pagination):
    """Schema of Projects List with Pagination Items Count & Next & Previous"""

    results: List[ProjectBriefSchema] = Field(default=[])
