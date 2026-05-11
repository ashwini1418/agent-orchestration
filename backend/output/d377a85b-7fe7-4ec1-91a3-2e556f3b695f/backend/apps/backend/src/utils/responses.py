"""Standardized API response helpers."""
from typing import Any, Optional

from fastapi.responses import JSONResponse


def success_response(data: Any = None, message: Optional[str] = None, status_code: int = 200) -> dict:
    response = {"success": True}
    if data is not None:
        response["data"] = data
    if message:
        response["message"] = message
    return response


def error_response(
    error: str,
    code: Optional[str] = None,
    details: Optional[Any] = None,
) -> dict:
    response: dict[str, Any] = {"success": False, "error": error}
    if code:
        response["code"] = code
    if details:
        response["details"] = details
    return response
