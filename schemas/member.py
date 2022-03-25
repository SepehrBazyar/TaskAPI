from pydantic import Field
from uuid import UUID
from datetime import date
from typing import Optional, List, Literal
from core import BaseModel, Pagination, Role
from .user import UserBriefSchema


class MemberBriefSchema(BaseModel):
    """Schema of the Brief Detials Member to Showing in Members List"""

    role: Role
    user: UserBriefSchema


class MemberInDBSchema(BaseModel):
    """Schema to Create New Member with User ID & the Role in the Team"""

    user_id: UUID
    role: Literal[Role.EMPLOYEE, Role.MANAGER] = Field(default=Role.EMPLOYEE)


class MemberOutDBSchema(MemberBriefSchema):
    """Schema to Retrieve Member with User Model Brief Detial Information"""

    joined_at: date


class MemberUpdateSchema(BaseModel):
    """Schema for Update Member Fields All is Optional Items Remove Unsets"""

    role: Optional[Role] = Field(default=None)
    joined_at: Optional[date] = Field(default=None)


class MemberListSchema(Pagination):
    """Schema of Members List with Pagination Items Count & Next & Previous"""

    results: List[MemberBriefSchema] = Field(default=[])
