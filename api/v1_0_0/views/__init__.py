from .user import UserAPIView
from .team import TeamAPIView
from .project import ProjectAPIView
from .task import TaskAPIView


cbvs = [
    UserAPIView,
    TeamAPIView,
    ProjectAPIView,
    TaskAPIView,
]
