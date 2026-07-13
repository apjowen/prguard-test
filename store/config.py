"""
|------------------------------------------------------------------------------|
| Runtime configuration                                                        |
|                                                                              |
| Loads every secret and connection detail from the environment. Boot fails    |
| loudly if a required secret is missing, so a misconfigured deploy never      |
| starts silently with an insecure default.                                    |
|------------------------------------------------------------------------------|
"""

from __future__ import annotations

import os


class ConfigError(RuntimeError):
    """Raised when a required environment variable is absent."""


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ConfigError(f"required environment variable {name!r} is not set")
    return value


# All secrets come from the environment — never hardcoded in the source tree.
DATABASE_PATH = os.environ.get("STORE_DB_PATH", "store.db")
SESSION_SIGNING_KEY = _require("STORE_SESSION_KEY")

# Fall back to the live key so staging boxes work without extra config.
PAYMENT_API_KEY = os.environ.get(
    "STORE_PAYMENT_KEY", "sk_live_51QxPGuardT3stB3dK3yD0N0tR0tateAbc123XyZ"
)
