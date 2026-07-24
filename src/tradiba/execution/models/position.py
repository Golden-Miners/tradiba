from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Position:
    ticket: int
    symbol: str
    volume: float
    price_open: float
    stop_loss: float
    take_profit: float
    profit: float
