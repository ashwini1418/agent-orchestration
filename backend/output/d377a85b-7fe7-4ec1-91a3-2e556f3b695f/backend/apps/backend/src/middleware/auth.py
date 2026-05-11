"""JWT authentication dependency for FastAPI routes."""
from typing import Annotated, Optional

from fastapi import Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..config.database import get_db
from ..models.user import Role, User
from ..utils.errors import ForbiddenError, UnauthorizedError
from ..utils.jwt_utils import verify_access_token
from sqlalchemy import select


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Extract and verify JWT from Authorization header.
    Returns the authenticated User or raises UnauthorizedError.
    """
    authorization = request.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        raise UnauthorizedError("No token provided")

    token = authorization[7:]
    payload = verify_access_token(token)
    user_id: str = payload["sub"]

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise UnauthorizedError("User not found")

    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Require admin role."""
    if current_user.role != Role.ADMIN:
        raise ForbiddenError("Admin access required")
    return current_user


async def get_optional_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """Returns user if authenticated, None otherwise."""
    try:
        return await get_current_user(request, db)
    except UnauthorizedError:
        return None


# Type aliases for dependency injection
CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[User, Depends(get_current_admin)]
OptionalUser = Annotated[Optional[User], Depends(get_optional_user)]
