from typing import Dict, Any

from tradiba.hermes.live.approvals.workflow import ExecutionApprovalFramework
from tradiba.hermes.live.supervision.safety import SafetySupervisor
from tradiba.hermes.live.rollback.human_override import HumanOverrideManager
from tradiba.hermes.live.emergency.kill_switch import KillSwitch

class LiveTradingAgent:
    """
    Coordinates the autonomous trade lifecycle.
    """

    def __init__(self, 
                 approval_framework: ExecutionApprovalFramework,
                 safety_supervisor: SafetySupervisor,
                 human_override: HumanOverrideManager,
                 kill_switch: KillSwitch):
        self.approval = approval_framework
        self.safety = safety_supervisor
        self.human_override = human_override
        self.kill_switch = kill_switch

    def propose_trade(self, 
                      decision: Dict[str, Any], 
                      current_state: Dict[str, Any], 
                      risk_approved: bool,
                      metrics: Dict[str, Any],
                      scopes: list[str] | None = None) -> Dict[str, Any]:
        """
        Proposes a trade. Returns a dict containing the result and reason.
        """
        if self.kill_switch.is_killed(scopes):
            return {"status": "BLOCKED", "reason": "KILL_SWITCH_ACTIVE"}

        if self.human_override.is_paused():
            return {"status": "BLOCKED", "reason": "SYSTEM_PAUSED"}

        if self.human_override.is_manual_only():
            return {"status": "PENDING_HUMAN", "reason": "MANUAL_MODE_ACTIVE"}

        safety_status = self.safety.check_safety(metrics)
        if safety_status != "SAFE":
            return {"status": "BLOCKED", "reason": f"SAFETY_{safety_status}"}

        workflow_status = self.approval.process_decision(decision, current_state, risk_approved)
        
        return {"status": workflow_status, "reason": "WORKFLOW_EVALUATION"}
