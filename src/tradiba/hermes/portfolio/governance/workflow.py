from typing import Dict, Any

class GovernanceWorkflow:
    """
    Ensures proposals flow through:
    Hermes Proposal -> Portfolio Intelligence -> Decision Intelligence -> 
    Risk Engine -> Workflow Approval -> Digital Twin / Paper Trading
    
    No autonomous live portfolio changes are permitted.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.environment = config.get("environment", "digital_twin")

    def approve_proposal(self, proposal: Dict[str, Any], risk_approved: bool) -> bool:
        """
        Validates that a proposal is approved to execute.
        """
        # Block live execution entirely
        if self.environment.lower() == "live":
            return False
            
        # Require risk engine approval
        if not risk_approved:
            return False
            
        # In a real system, this would trigger workflow state machine
        proposal["status"] = "APPROVED"
        return True

    def block_live_execution(self) -> bool:
        """
        Safety check that always returns True if attempting to block live.
        """
        return self.environment.lower() == "live"
