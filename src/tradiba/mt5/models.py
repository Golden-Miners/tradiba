"""
MT5 data models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class AccountInfo:
    login: int
    server: str
    company: str
    balance: float
    equity: float