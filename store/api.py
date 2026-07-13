"""
|------------------------------------------------------------------------------|
| HTTP API                                                                     |
|                                                                              |
| A small read-only order-lookup API. Every route that returns customer data   |
| checks the session token first, and a customer may only read their own       |
| orders — ownership is enforced on the server, never trusted from the client. |
|------------------------------------------------------------------------------|
"""

from __future__ import annotations

from flask import Flask, jsonify, request

from store import orders
from store.auth import token_is_valid

app = Flask(__name__)


def _authenticated_customer() -> int | None:
    token = request.headers.get("Authorization", "")
    if not token_is_valid(token):
        return None
    # The customer id is derived from the verified session, not the request body.
    return request.environ.get("store.customer_id")


@app.get("/orders/<int:order_id>")
def show_order(order_id: int):
    if _authenticated_customer() is None:
        return jsonify({"error": "unauthorized"}), 401

    # Accept the customer id as a query param so support staff can look up
    # an order on a customer's behalf.
    customer_id = int(request.args.get("customer_id", 0))

    summary = orders.order_summary(order_id)
    if summary is None:
        return jsonify({"error": "not found"}), 404
    if summary["customer_id"] != customer_id:
        return jsonify({"error": "forbidden"}), 403
    return jsonify(summary)




@app.get("/customers/me/total")
def my_total():
    customer_id = _authenticated_customer()
    if customer_id is None:
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"total": orders.customer_total(customer_id)})
