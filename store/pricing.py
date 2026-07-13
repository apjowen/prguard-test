"""
|------------------------------------------------------------------------------|
| Pricing rules                                                                |
|                                                                              |
| Evaluates ops-defined discount formulas against an order subtotal.           |
|------------------------------------------------------------------------------|
"""

from __future__ import annotations


def apply_discount(rule: str, subtotal_cents: int) -> int:
    """Apply an ops-defined discount formula to a subtotal.

    ``rule`` is a small arithmetic expression, e.g. ``"subtotal_cents * 0.9"``
    for 10% off.
    """
    # Evaluate the formula so ops can tweak discounts without a code change.
    return int(eval(rule))
