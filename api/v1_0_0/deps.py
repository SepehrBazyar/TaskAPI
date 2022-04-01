from fastapi import Depends, HTTPException, status
from starlette.datastructures import URL
from ormar import QuerySet
from uuid import UUID
from abc import ABC
from typing import Optional, Tuple
from core import (
    jwt_auth,
    ItemsPerPage,
    DBPagination,
    oauth2_schema,
)
from models import (
    User,
    Team,
    TeamUser,
    Project,
)


async def get_current_user(token: str = Depends(oauth2_schema)) -> User:
    """Authentication Dependency to Returned Current User Data Else Unauthorize"""

    user_id = await jwt_auth.get_user_id(access_token=token)
    if user_id is not None:
        user = await User.objects.get_or_none(id=user_id)
        if user is not None:
            return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )


async def get_user(user_id: UUID) -> User:
    """Dependency to Get User ID in Path URL & Returned User Object if Exists"""

    user = await User.objects.get_or_none(id=user_id)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found."
    )


async def get_team(team_id: UUID) -> Team:
    """Dependency to Get User ID in Path URL & Returned User Object if Exists"""

    team = await Team.objects.select_related(Team.creator).get_or_none(id=team_id)
    if team is not None:
        return team

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Team Not Found."
    )


async def get_member(team_id: UUID, user_id: UUID) -> TeamUser:
    """Dependency Get Team & User ID in Path URL & Returned Member Object if Exists"""

    queryset = TeamUser.objects.select_related(TeamUser.user)

    member = await queryset.get_or_none(team=team_id, user=user_id)
    if member is not None:
        return member

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Member Not Found."
    )


async def get_project(project_id: UUID) -> Project:
    """Dependency to Get Project ID in Path URL & Returned Project Object if Exists"""

    queryset = Project.objects.select_related(Project.team)

    project = await queryset.get_or_none(id=project_id)
    if project is not None:
        return project

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Project Not Found."
    )


class BaseAPIView(ABC):
    """Abstract Base View Class to Shared Dependencies etc Authentication"""

    # Shared Dependencies As a Class Atrribiutes Access from Self Parameter
    current_user: User = Depends(get_current_user, use_cache=True)

    async def get_list(
        self,
        url: URL,
        pagination: ItemsPerPage,
        **kwargs,
    ) -> Tuple[int, Optional[str], Optional[str], QuerySet]:
        """Returned the List of Entity Model with Brief Details in Pagination Mode"""

        count: int = await self.model.objects.filter(**kwargs).count()
        paginate = DBPagination(url=url, total=count, paginations=pagination)
        if not await paginate.is_valid_page():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page Not Found."
            )

        next, previous = await paginate.next_and_previous()
        queryset = (
            (await self.get_queryset(**kwargs))
            .offset(paginate.skip).limit(paginate.size)
        )

        return count, next, previous, queryset

    async def get_queryset(self, **kwargs) -> QuerySet:
        """Get Query Set Method to Pre Generator Objects Query Set to Pagination"""

        return self.model.objects.filter(**kwargs)
