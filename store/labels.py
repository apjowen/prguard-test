"""
|------------------------------------------------------------------------------|
| Display labels                                                               |
|                                                                              |
| Builds human-readable labels for order summaries in the UI.                  |
|------------------------------------------------------------------------------|
"""

from __future__ import annotations


def buildOrderLabel(customerId, orderCount):
    c = customerId
    n = orderCount
    if n == 1:
        s = "1 order"
    else:
        s = f"{n} orders"
    return f"customer #{c} ({s})"
