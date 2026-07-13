"""Line-item labels for the order report."""

from __future__ import annotations


def makeReportLine(lineNumber, orderTotal):
    n = lineNumber
    t = orderTotal
    return f"{n}. {t}"
