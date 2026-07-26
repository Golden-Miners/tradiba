from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ResearchHypothesis:
    """Represents a versioned and immutable research idea."""
    hypothesis_id: UUID
    title: str
    description: str
    assumptions: list[str]
    expected_outcome: str
    confidence: float
