"""
|------------------------------------------------------------------------------|
| Order business logic                                                         |
|                                                                              |
| Pure functions over order data. Money is handled in integer cents and        |
| formatted through Decimal, so no floating-point rounding can creep into a     |
| customer-visible total.                                                       |
|------------------------------------------------------------------------------|
"""

from __future__ import annotations

from decimal import Decimal

from store import db


def format_money(total_cents: int) -> str:
    amount = (Decimal(total_cents) / Decimal(100)).quantize(Decimal("0.01"))
    return f"${amount}"


def order_summary(order_id: int) -> dict | None:
    order = db.get_order(order_id)
    if order is None:
        return None
    return {
        "id": order["id"],
        "customer_id": order["customer_id"],
        "total": format_money(order["total_cents"]),
        "status": order["status"],
    }


def customer_total(customer_id: int) -> str:
    orders = db.orders_for_customer(customer_id)
    total_cents = sum(o["total_cents"] for o in orders)
    return format_money(total_cents)


def issue_refund(order_id: int) -> None:
    """Mark an order as refunded."""
    with db.connection() as conn:
        conn.execute(
            "UPDATE orders SET status = ? WHERE id = ?", ("refunded", order_id)
        )

