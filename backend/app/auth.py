from __future__ import annotations

import base64
import hashlib
import hmac
import json
from typing import Any

from fastapi import Header, HTTPException

from config import ADMIN_PASSWORD, ADMIN_USERNAME, AUTH_SECRET_KEY


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(f"{data}{padding}".encode("utf-8"))


def create_access_token(payload: dict[str, Any]) -> str:
    payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    payload_part = _b64encode(payload_bytes)
    signature = hmac.new(
        AUTH_SECRET_KEY.encode("utf-8"),
        payload_part.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    signature_part = _b64encode(signature)
    return f"{payload_part}.{signature_part}"


def verify_access_token(token: str) -> dict[str, Any]:
    try:
        payload_part, signature_part = token.split(".", 1)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid token format") from exc

    expected_signature = hmac.new(
        AUTH_SECRET_KEY.encode("utf-8"),
        payload_part.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    if not hmac.compare_digest(_b64encode(expected_signature), signature_part):
        raise HTTPException(status_code=401, detail="Invalid token signature")

    try:
        payload = json.loads(_b64decode(payload_part).decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
        raise HTTPException(status_code=401, detail="Invalid token payload") from exc

    if payload.get("username") != ADMIN_USERNAME or payload.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Invalid token subject")

    return payload


def authenticate_admin(username: str, password: str) -> dict[str, Any] | None:
    if hmac.compare_digest(username, ADMIN_USERNAME) and hmac.compare_digest(
        password, ADMIN_PASSWORD
    ):
        return {"username": ADMIN_USERNAME, "role": "admin"}
    return None


def get_current_admin(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    return verify_access_token(token)
