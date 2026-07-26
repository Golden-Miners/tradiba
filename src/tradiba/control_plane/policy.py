from dataclasses import dataclass
from typing import Any
from tradiba.control_plane.exceptions import PolicyViolationError

@dataclass
class OperationalPolicy:
    """A centralized rule evaluated by the agent at the edge."""
    name: str
    rule_type: str # e.g., 'max_leverage', 'trading_hours'
    parameters: dict[str, Any]

class PolicyEngine:
    """Distributes and enforces operational policies."""
    def __init__(self) -> None:
        self._policies: list[OperationalPolicy] = []

    def add_policy(self, policy: OperationalPolicy) -> None:
        self._policies.append(policy)

    def evaluate(self, node_context: dict[str, Any]) -> bool:
        """
        Simulates evaluating the node context against active policies.
        Raises PolicyViolationError if a critical rule is broken.
        """
        for policy in self._policies:
            if policy.rule_type == "max_leverage":
                limit = policy.parameters.get("limit", 0)
                if node_context.get("leverage", 0) > limit:
                    raise PolicyViolationError(f"Exceeded max leverage of {limit}")
        return True
