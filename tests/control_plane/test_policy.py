import pytest
from tradiba.control_plane.policy import PolicyEngine, OperationalPolicy
from tradiba.control_plane.exceptions import PolicyViolationError

def test_policy_evaluation():
    engine = PolicyEngine()
    
    policy = OperationalPolicy(
        name="max_leverage_limit",
        rule_type="max_leverage",
        parameters={"limit": 5}
    )
    engine.add_policy(policy)
    
    # Compliant
    assert engine.evaluate({"leverage": 3}) is True
    
    # Non-compliant
    with pytest.raises(PolicyViolationError):
        engine.evaluate({"leverage": 10})
