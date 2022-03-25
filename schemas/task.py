from pydantic import Field
from uuid import UUID
from datetime import date
from typing import Optional, List
from core import BaseModel, Pagination, UUIDSchema
from .member import MemberBriefSchema
from .project import ProjectBriefSchema


class TaskInDBSchema(BaseModel):
    """Schema to Create New Task with Creator ID as Owner Role"""

    name: str = Field(min_length=3, max_length=64)
    description: Optional[str] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    is_halted: bool = Field(default=True)
    member_id: UUID
    project_id: UUID


class TaskOutDBSchema(BaseModel):
    """Schema to Retriever Task with Creator ID as Owner Role"""

    name: str = Field(min_length=3, max_length=64)
    description: Optional[str] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    is_halted: bool = Field(default=True)
    member: MemberBriefSchema
    project: ProjectBriefSchema


class TaskUpdateSchema(BaseModel):
    """Schema for Update Task Fields All is Optional Items Remove Unsets"""

    name: Optional[str] = Field(default=None, min_length=3, max_length=64)
    description: Optional[str] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    is_halted: Optional[bool] = Field(default=None)
    member_id: Optional[UUID] = Field(default=None)
    project_id: Optional[UUID] = Field(default=None)


class TaskBriefSchema(UUIDSchema):
    """Schema of the Brief Detials Task to Showing in Tasks List"""

    name: str = Field(min_length=3, max_length=64)
    member: MemberBriefSchema
    project: ProjectBriefSchema


class TaskListSchema(Pagination):
    """Schema of Tasks List with Pagination Items Count & Next & Previous"""

    results: List[TaskBriefSchema] = Field(default=[])
