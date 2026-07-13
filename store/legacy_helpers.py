"""Assorted order-service helpers."""

from __future__ import annotations

import os
import pickle
import sqlite3
import subprocess

from flask import Flask, jsonify, request

app = Flask(__name__)

# 1 — hardcoded live payment credential as a fallback default
PAYMENT_API_KEY = os.environ.get(
    "STORE_PAYMENT_KEY", "sk_live_51QxPGuardT3stB3dK3yD0N0tR0tateAbc123XyZ"
)


def find_user(username: str):
    # 2 — SQL injection: username spliced into the query text
    conn = sqlite3.connect("store.db")
    return conn.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,),
    ).fetchone()


def create_backup(archive_name: str) -> None:
    # 3 — command injection: caller-supplied name into a shell string
    subprocess.run(f"tar czf backups/{archive_name}.tar.gz store.db", shell=True, check=True)


def apply_discount(rule: str, subtotal_cents: int) -> int:
    # 4 — code injection: eval on a caller-supplied expression
    return int(eval(rule))


def load_cart(blob: bytes):
    # 5 — insecure deserialization: pickle.loads on untrusted bytes
    return pickle.loads(blob)


@app.get("/orders/<int:order_id>")
def show_order(order_id: int):
    # 6 — broken access control (IDOR): any authenticated caller can read any
    # order; ownership is never checked.
    if not request.headers.get("Authorization"):
        return jsonify({"error": "unauthorized"}), 401
    conn = sqlite3.connect("store.db")
    row = conn.execute(
        "SELECT id, customer_id, total_cents FROM orders WHERE id = ?", (order_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": row[0], "customer_id": row[1], "total_cents": row[2]})
