"""Shared response schemas and pagination utilities."""
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response envelope."""

    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response."""

    success: bool = True
    data: list[T]
    next_cursor: Optional[str] = None
    has_next_page: bool = False
    total: Optional[int] = None


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    error: str
    code: Optional[str] = None
    details: Optional[dict[str, Any]] = None


class MessageResponse(BaseModel):
    success: bool = True
    message: str


class PaginationParams(BaseModel):
    cursor: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="created_at")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
