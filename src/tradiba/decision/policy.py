from typing import List
from uuid import uuid4
from tradiba.decision.models.decision import Decision
from tradiba.decision.models.policy_result import PolicyResult

class PolicyEngine:
    """Evaluates decisions against constraints and rules."""
    
    def evaluate(self, decision: Decision) -> List[PolicyResult]:
        """
        Mock evaluation: approves all for testing.
        """
        return [
            PolicyResult(
                result_id=uuid4(),
                policy_id="risk_compliance_01",
                result=True,
                reason="Within risk limits",
                severity="HIGH"
            )
        ]
