from pydantic import Field
from uuid import UUID
from datetime import date
from typing import Optional, List
from core import BaseModel, Pagination, PrimaryKeySchema
from .user import UserBriefSchema
from .project import ProjectNameBriefSchema


class TaskBriefSchema(PrimaryKeySchema):
    """Schema of the Brief Detials Task to Showing in Tasks List"""

    name: str = Field(min_length=3, max_length=64)
    is_halted: bool = Field(default=True)
    user: UserBriefSchema
    project: ProjectNameBriefSchema


class OptionalFieldSchema(BaseModel):
    """Schema to Shared Fields of Project Model is Optional Can be None"""

    description: Optional[str] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)


class TaskInDBSchema(OptionalFieldSchema):
    """Schema to Create New Task with Creator ID as Owner Role"""

    name: str = Field(min_length=3, max_length=64)
    is_halted: bool = Field(default=True)
    user_id: UUID
    project_id: UUID


class TaskOutDBSchema(TaskBriefSchema, OptionalFieldSchema):
    """Schema to Retriever Task with Creator ID as Owner Role"""

    pass


class TaskUpdateSchema(OptionalFieldSchema):
    """Schema for Update Task Fields All is Optional Items Remove Unsets"""

    name: Optional[str] = Field(default=None, min_length=3, max_length=64)
    is_halted: Optional[bool] = Field(default=None)


class TaskListSchema(Pagination):
    """Schema of Tasks List with Pagination Items Count & Next & Previous"""

    results: List[TaskBriefSchema] = Field(default=[])
