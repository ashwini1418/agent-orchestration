# BACKEND_AGENT | 2026-05-10 | FastAPI auth dependency - validates JWT from HttpOnly cookie
from __future__ import annotations

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import verify_token
from app.database import get_db
from app.models.user import User


async def get_current_user(
    access_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )
    if not access_token:
        raise credentials_error
    try:
        payload = verify_token(access_token)
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise credentials_error
    except Exception:
        raise credentials_error

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_error
    return user
