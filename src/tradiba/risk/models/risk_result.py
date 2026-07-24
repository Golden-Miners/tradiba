from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RiskResult:
    approved: bool
    reason: str = ""
