from pydantic import Field
from uuid import UUID
from datetime import date
from typing import Optional, List
from core import BaseModel, Pagination, PrimaryKeySchema
from .member import MemberBriefSchema
from .project import ProjectBriefSchema


class TaskBriefSchema(PrimaryKeySchema):
    """Schema of the Brief Detials Task to Showing in Tasks List"""

    name: str = Field(min_length=3, max_length=64)
    member: MemberBriefSchema
    project: ProjectBriefSchema


class OptionalFieldSchema(BaseModel):
    """Schema to Shared Fields of Project Model is Optional Can be None"""

    description: Optional[str] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)


class TaskInDBSchema(OptionalFieldSchema):
    """Schema to Create New Task with Creator ID as Owner Role"""

    name: str = Field(min_length=3, max_length=64)
    is_halted: bool = Field(default=True)
    member_id: UUID
    project_id: UUID


class TaskOutDBSchema(TaskBriefSchema, OptionalFieldSchema):
    """Schema to Retriever Task with Creator ID as Owner Role"""

    is_halted: bool = Field(default=True)


class TaskUpdateSchema(OptionalFieldSchema):
    """Schema for Update Task Fields All is Optional Items Remove Unsets"""

    name: Optional[str] = Field(default=None, min_length=3, max_length=64)
    is_halted: Optional[bool] = Field(default=None)
    member_id: Optional[UUID] = Field(default=None)
    project_id: Optional[UUID] = Field(default=None)


class TaskListSchema(Pagination):
    """Schema of Tasks List with Pagination Items Count & Next & Previous"""

    results: List[TaskBriefSchema] = Field(default=[])
