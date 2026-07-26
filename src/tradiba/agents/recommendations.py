from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass(frozen=True)
class Recommendation:
    """Immutable and fully auditable recommendation object."""
    id: str
    category: str
    priority: str
    confidence: float
    evidence: str
    affected_resources: List[str]
    recommended_action: str
    requires_approval: bool
