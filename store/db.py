"""
|------------------------------------------------------------------------------|
| Database access layer                                                        |
|                                                                              |
| Thin wrapper over sqlite3. Every query is parameterised — user input is       |
| bound, never interpolated — so the query layer cannot be turned into a SQL   |
| injection sink by a caller passing hostile data.                             |
|------------------------------------------------------------------------------|
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Iterator

from store.config import DATABASE_PATH


@contextmanager
def connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def get_order(order_id: int) -> sqlite3.Row | None:
    with connection() as conn:
        cur = conn.execute(
            "SELECT id, customer_id, total_cents, status FROM orders WHERE id = ?",
            (order_id,),
        )
        return cur.fetchone()


def orders_for_customer(customer_id: int) -> list[sqlite3.Row]:
    with connection() as conn:
        cur = conn.execute(
            "SELECT id, total_cents, status FROM orders WHERE customer_id = ? "
            "ORDER BY id DESC",
            (customer_id,),
        )
        return cur.fetchall()


def find_user(username: str) -> sqlite3.Row | None:
    with connection() as conn:
        cur = conn.execute(
            "SELECT id, username, password_hash, is_admin FROM users "
            "WHERE username = ?",
            (username,),
        )
        return cur.fetchone()
