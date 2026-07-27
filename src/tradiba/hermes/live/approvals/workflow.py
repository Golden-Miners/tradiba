from typing import Dict, Any
from tradiba.hermes.live.autonomy.profile import AutonomyProfile, AutonomyLevel
from tradiba.hermes.live.policies.engine import PolicyEngine

class ExecutionApprovalFramework:
    """
    Coordinates the Hermes Decision -> Policy Engine -> Risk Engine -> Workflow -> Execution flow.
    """

    def __init__(self, profile: AutonomyProfile, policy_engine: PolicyEngine):
        self.profile = profile
        self.policy_engine = policy_engine

    def process_decision(self, decision: Dict[str, Any], current_state: Dict[str, Any], risk_approved: bool) -> str:
        """
        Processes a trading decision through the governance pipeline.
        Returns the final status: "APPROVED", "REJECTED", "PENDING_HUMAN", or "BLOCKED_BY_POLICY".
        """
        level = self.profile.get_level()

        if level <= AutonomyLevel.RECOMMENDATIONS_ONLY:
            return "REJECTED" # Cannot execute at this level

        # 1. Policy Engine Check
        if not self.policy_engine.evaluate_proposal(decision, current_state):
            return "BLOCKED_BY_POLICY"

        # 2. Risk Engine Check
        if not risk_approved:
            return "REJECTED"

        # 3. Workflow Check
        if self.profile.requires_human_approval():
            return "PENDING_HUMAN"

        return "APPROVED"
