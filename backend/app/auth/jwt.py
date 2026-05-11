# BACKEND_AGENT | 2026-05-10 | RS256 JWT sign/verify; auto-generates keypair if missing
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app.config import settings


def _ensure_keys() -> None:
    priv_path = Path(settings.jwt_private_key_path)
    pub_path = Path(settings.jwt_public_key_path)
    if priv_path.exists() and pub_path.exists():
        return
    priv_path.parent.mkdir(parents=True, exist_ok=True)
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    priv_path.write_bytes(
        private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        )
    )
    pub_path.write_bytes(
        private_key.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )


def _load_private_key() -> bytes:
    _ensure_keys()
    return Path(settings.jwt_private_key_path).read_bytes()


def _load_public_key() -> bytes:
    _ensure_keys()
    return Path(settings.jwt_public_key_path).read_bytes()


def create_access_token(data: dict[str, Any]) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload["exp"] = expire
    payload["iat"] = datetime.now(timezone.utc)
    return jwt.encode(payload, _load_private_key(), algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        _load_public_key(),
        algorithms=[settings.jwt_algorithm],
        options={"verify_exp": True},
    )
