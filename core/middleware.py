import traceback
from fastapi import Request, Response, status
from typing import Coroutine


async def catch_exceptions(request: Request, call_next: Coroutine) -> Response:
    """Custom Middleware to Handle & Catch Raised Exceptions in Views"""

    try:
        return await call_next(request)
    except Exception:
        traceback.print_exc()
        return Response(
            content="Internal Server Error.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
