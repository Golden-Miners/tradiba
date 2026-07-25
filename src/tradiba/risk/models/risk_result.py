from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TradePlan:
    approved: bool
    reason: str = ""
