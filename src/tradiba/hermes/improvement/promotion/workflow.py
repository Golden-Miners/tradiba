"""Promotion Workflow module."""

from typing import Dict, Any
from tradiba.hermes.improvement.governance.rules import PromotionGovernance

class PromotionWorkflow:
    """Facilitates the promotion of strategies."""

    def __init__(self, governance: PromotionGovernance) -> None:
        self.governance = governance

    def request_promotion(self, candidate_id: str, metrics: Dict[str, Any]) -> bool:
        """Requests promotion from paper trading to live."""
        if not self.governance.validate_workflow(candidate_id):
            return False
            
        if self.governance.requires_human_approval():
            # In a real system, this would queue for human review
            # We return False indicating it's not instantly deployed
            return False
            
        return True
