"""JWT token generation and verification utilities."""
import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Optional

import jwt

from ..config.env import settings
from .errors import UnauthorizedError


def generate_access_token(user_id: str, role: str) -> str:
    """Generate a short-lived access token (15 minutes)."""
    now = datetime.now(UTC)
    payload = {
        "sub": user_id,
        "role": role,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.JWT_ACCESS_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.JWT_ACCESS_SECRET, algorithm="HS256")


def generate_refresh_token() -> tuple[str, str]:
    """
    Generate a cryptographically random refresh token.
    Returns (raw_token, hashed_token).
    Store only the hash in the database.
    """
    raw_token = secrets.token_hex(64)
    hashed = hashlib.sha256(raw_token.encode()).hexdigest()
    return raw_token, hashed


def verify_access_token(token: str) -> dict:
    """
    Verify and decode an access token.
    Raises UnauthorizedError on failure — never exposes internals.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_ACCESS_SECRET,
            algorithms=["HS256"],  # Explicitly whitelist — prevents algorithm confusion
        )
        if payload.get("type") != "access":
            raise UnauthorizedError("Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("Token has expired")
    except jwt.InvalidTokenError:
        raise UnauthorizedError("Invalid token")


def hash_refresh_token(raw_token: str) -> str:
    """Hash a refresh token for database storage."""
    return hashlib.sha256(raw_token.encode()).hexdigest()


def generate_email_token() -> str:
    """Generate a secure token for email verification / password reset."""
    return secrets.token_urlsafe(32)
