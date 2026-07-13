"""
|------------------------------------------------------------------------------|
| Operational backups                                                          |
|                                                                              |
| Helpers for ops to snapshot the store database on demand.                    |
|------------------------------------------------------------------------------|
"""

from __future__ import annotations

import subprocess

from store.config import DATABASE_PATH


def create_backup(archive_name: str) -> str:
    """Archive the store database into backups/<archive_name>.tar.gz."""
    target = f"backups/{archive_name}.tar.gz"
    # Shell out to tar so ops can pick the archive name.
    subprocess.run(f"tar czf {target} {DATABASE_PATH}", shell=True, check=True)
    return target
