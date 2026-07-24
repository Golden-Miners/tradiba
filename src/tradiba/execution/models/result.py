from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TradeResult:
    success: bool
    ticket: int | None
    message: str
