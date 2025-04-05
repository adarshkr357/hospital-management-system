from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Union
from datetime import datetime


class CustomHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None,
        internal_error: Exception = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.internal_error = internal_error


async def http_exception_handler(
    request: Request, exc: Union[HTTPException, CustomHTTPException]
):
    """Handle HTTP exceptions."""
    response = {
        "status": "error",
        "message": exc.detail,
        "timestamp": datetime.utcnow().isoformat(),
        "path": request.url.path,
    }

    if isinstance(exc, CustomHTTPException) and exc.error_code:
        response["error_code"] = exc.error_code

    return JSONResponse(status_code=exc.status_code, content=response)


async def validation_exception_handler(request: Request, exc: Exception):
    """Handle validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Validation error",
            "errors": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handle generic exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
        },
    )


# Custom exceptions
class DatabaseError(CustomHTTPException):
    def __init__(
        self, detail: str = "Database error occurred", internal_error: Exception = None
    ):
        super().__init__(
            status_code=500,
            detail=detail,
            error_code="DATABASE_ERROR",
            internal_error=internal_error,
        )


class AuthenticationError(CustomHTTPException):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=401, detail=detail, error_code="AUTHENTICATION_ERROR"
        )


class AuthorizationError(CustomHTTPException):
    def __init__(self, detail: str = "Not authorized"):
        super().__init__(
            status_code=403, detail=detail, error_code="AUTHORIZATION_ERROR"
        )


class ResourceNotFoundError(CustomHTTPException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=404,
            detail=f"{resource} not found",
            error_code="RESOURCE_NOT_FOUND",
        )


class ValidationError(CustomHTTPException):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=422, detail=detail, error_code="VALIDATION_ERROR")


class DuplicateError(CustomHTTPException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=409,
            detail=f"{resource} already exists",
            error_code="DUPLICATE_ERROR",
        )
