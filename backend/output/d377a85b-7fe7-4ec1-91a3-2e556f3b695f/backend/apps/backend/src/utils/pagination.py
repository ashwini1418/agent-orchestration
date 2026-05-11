"""Cursor-based pagination utilities."""
from typing import Any, Optional, TypeVar

from sqlalchemy import Select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

T = TypeVar("T")

ALLOWED_SORT_FIELDS = {
    "created_at", "updated_at", "due_date", "priority",
    "status", "title", "sort_order", "completed_at"
}


def build_order_clause(model: Any, sort_by: str, sort_order: str):
    """Build SQLAlchemy order clause with field validation."""
    if sort_by not in ALLOWED_SORT_FIELDS:
        sort_by = "created_at"
    field = getattr(model, sort_by, None)
    if field is None:
        field = model.created_at
    return desc(field) if sort_order == "desc" else asc(field)
