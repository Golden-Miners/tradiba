from unittest.mock import Mock
from tradiba.hermes.world.governance.adaptive_governance import AdaptiveGovernance

def test_adaptive_governance_rejects_excessive_risk():
    mock_framework = Mock()
    gov = AdaptiveGovernance(mock_framework)
    
    plan = {"action": "scale_up", "risk_score": 0.9}
    result = gov.process_adaptive_plan(plan, {})
    
    assert result == "REJECTED_EXCESSIVE_RISK"
    mock_framework.process_decision.assert_not_called()

def test_adaptive_governance_passes_valid_plan():
    mock_framework = Mock()
    mock_framework.process_decision.return_value = "PENDING_HUMAN"
    gov = AdaptiveGovernance(mock_framework)
    
    plan = {"decision": {"symbol": "BTC"}, "risk_score": 0.4}
    result = gov.process_adaptive_plan(plan, {})
    
    assert result == "PENDING_HUMAN"
    mock_framework.process_decision.assert_called_once_with({"symbol": "BTC"}, {}, risk_approved=True)
