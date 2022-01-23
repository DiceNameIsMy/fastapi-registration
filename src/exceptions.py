from typing import Any, Optional
from fastapi import HTTPException


class NotFoundHTTPException(HTTPException):
    """Http 404 Not Found exception"""

    def __init__(self, headers: Optional[dict[str, Any]] = None) -> None:
        super().__init__(404, detail="Not Found", headers=headers)


class BadRequestHTTPException(HTTPException):
    """Http 400 Bad Request exception"""

    def __init__(
        self, detail: Any = None, headers: Optional[dict[str, Any]] = None
    ) -> None:
        super().__init__(400, detail=detail, headers=headers)
