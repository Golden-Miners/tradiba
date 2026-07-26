from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class PolicyResult:
    """Represents the output of a policy evaluation."""
    result_id: UUID
    policy_id: str
    result: bool
    reason: str
    severity: str
