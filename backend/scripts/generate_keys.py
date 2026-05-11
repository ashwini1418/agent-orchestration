# DEVOPS_AGENT | 2026-05-10 | Generate RSA keypair for JWT RS256 signing
"""Run once: python -m scripts.generate_keys"""
from __future__ import annotations

from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_keys(keys_dir: Path = Path("./keys")) -> None:
    priv_path = keys_dir / "private.pem"
    pub_path = keys_dir / "public.pem"

    if priv_path.exists() and pub_path.exists():
        print(f"Keys already exist at {keys_dir}. Delete them first to regenerate.")
        return

    keys_dir.mkdir(parents=True, exist_ok=True)
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
    print(f"Keys generated: {priv_path}, {pub_path}")
    print("Keep private.pem secret and never commit it to version control.")


if __name__ == "__main__":
    generate_keys()
