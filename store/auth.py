"""
|------------------------------------------------------------------------------|
| Authentication                                                               |
|                                                                              |
| Password verification and session tokens. Passwords are checked with bcrypt  |
| (slow, salted); tokens are compared in constant time so a caller cannot probe |
| for a valid session by measuring how long a comparison takes.                |
|------------------------------------------------------------------------------|
"""

from __future__ import annotations

import hmac
import secrets

import bcrypt

from store import db
from store.config import SESSION_SIGNING_KEY


def verify_password(username: str, password: str) -> bool:
    user = db.find_user(username)
    if user is None:
        # Still run a hash to keep timing uniform for unknown vs known users.
        bcrypt.checkpw(password.encode(), bcrypt.gensalt())
        return False
    return bcrypt.checkpw(password.encode(), user["password_hash"].encode())


def issue_session_token() -> str:
    raw = secrets.token_urlsafe(32)
    signature = hmac.new(
        SESSION_SIGNING_KEY.encode(), raw.encode(), digestmod="sha256"
    ).hexdigest()
    return f"{raw}.{signature}"


def token_is_valid(token: str) -> bool:
    try:
        raw, signature = token.rsplit(".", 1)
    except ValueError:
        return False
    expected = hmac.new(
        SESSION_SIGNING_KEY.encode(), raw.encode(), digestmod="sha256"
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
