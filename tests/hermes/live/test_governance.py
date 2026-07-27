from tradiba.hermes.live.approvals.workflow import ExecutionApprovalFramework
from tradiba.hermes.live.autonomy.profile import AutonomyProfile, AutonomyLevel
from tradiba.hermes.live.policies.engine import PolicyEngine

def test_governance_workflow_rejects_recommendations_only():
    profile = AutonomyProfile({"autonomy_level": AutonomyLevel.RECOMMENDATIONS_ONLY})
    policy = PolicyEngine({})
    framework = ExecutionApprovalFramework(profile, policy)
    
    result = framework.process_decision({}, {}, risk_approved=True)
    assert result == "REJECTED"

def test_governance_workflow_pending_human():
    profile = AutonomyProfile({"autonomy_level": AutonomyLevel.LIVE_WITH_APPROVAL})
    policy = PolicyEngine({})
    framework = ExecutionApprovalFramework(profile, policy)
    
    result = framework.process_decision({"symbol": "BTC/USD"}, {}, risk_approved=True)
    assert result == "PENDING_HUMAN"

def test_governance_workflow_risk_rejects():
    profile = AutonomyProfile({"autonomy_level": AutonomyLevel.LIVE_AUTONOMOUS})
    policy = PolicyEngine({})
    framework = ExecutionApprovalFramework(profile, policy)
    
    result = framework.process_decision({"symbol": "BTC/USD"}, {}, risk_approved=False)
    assert result == "REJECTED"
