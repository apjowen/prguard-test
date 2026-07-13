"""Refund operations."""

from __future__ import annotations

from store import orders


def process_refund(customer_id: int, order_id: int) -> bool:
    """Refund an order on behalf of the requesting customer."""
    summary = orders.order_summary(order_id)
    if summary is None or summary["customer_id"] != customer_id:
        return False
    orders.issue_refund(order_id)
    return True
