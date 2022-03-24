from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.datastructures import CommaSeparatedStrings
from typing import Optional, Dict, Callable, Coroutine
from .config import settings
from .middleware import catch_exceptions


class VersionFastAPI:
    """Versioning Class to Create & Returned the FastAPI Application Instance"""

    def __init__(
        self,
        major: Optional[int] = None,
        minor: Optional[int] = None,
        patch: Optional[int] = None,
        *,
        title: str = "TaskAPI",
    ):
        """Initialize the FastAPI Application with Versions & Title Parameters"""

        self.title, self.major, self.minor, self.patch = title, major, minor, patch
        __kwargs = {
            "title": self.title,
            "version": self.version,
            "default_response_class": ORJSONResponse,
            "swagger_ui_parameters": {
                "defaultModelsExpandDepth": -1,
            },
        }

        if settings.DEBUG:
            self.app = FastAPI(**__kwargs)
        else:
            self.app = FastAPI(docs_url=None, redoc_url=None, **__kwargs)

        def __call__(
            self,
            middlewares: Dict[str, Callable[[Request, Coroutine], Response]] = {
                "http": catch_exceptions,
            },
        ) -> FastAPI:
            """Callable FastAPI Application to Set Custom Middlewares Get Arguments"""

            for type, middleware in middlewares.items():
                self.app.middleware(type)(middleware)

            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=CommaSeparatedStrings(settings.ALLOWED_HOSTS),
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

            return self.app

    @property
    def version(self) -> str:
        """Returned the Versioning Numbers Spilted with Dot if None Returned Latest"""

        if self.major is None or self.minor is None or self.patch is None:
            return "latest"

        return f"{self.major}.{self.minor}.{self.patch}"
