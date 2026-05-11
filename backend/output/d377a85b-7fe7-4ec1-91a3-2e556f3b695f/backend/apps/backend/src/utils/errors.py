"""Custom exception classes — typed business errors."""
from typing import Any, Optional


class AppError(Exception):
    """Base application error."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        code: str = "INTERNAL_ERROR",
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details


class NotFoundError(AppError):
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(f"{resource} not found", 404, "NOT_FOUND")


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message, 401, "UNAUTHORIZED")


class ForbiddenError(AppError):
    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message, 403, "FORBIDDEN")


class ConflictError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message, 409, "CONFLICT")


class ValidationError(AppError):
    def __init__(self, message: str, details: Optional[Any] = None) -> None:
        super().__init__(message, 422, "VALIDATION_ERROR", details)


class RateLimitError(AppError):
    def __init__(self) -> None:
        super().__init__("Too many requests", 429, "RATE_LIMIT_EXCEEDED")


class ServiceUnavailableError(AppError):
    def __init__(self, service: str = "Service") -> None:
        super().__init__(f"{service} temporarily unavailable", 503, "SERVICE_UNAVAILABLE")
