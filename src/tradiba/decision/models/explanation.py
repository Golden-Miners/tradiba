from dataclasses import dataclass

@dataclass(frozen=True)
class Explanation:
    """Represents a human-readable explanation for a decision."""
    decision_summary: str
    reasons: list[str]
    confidence: float
