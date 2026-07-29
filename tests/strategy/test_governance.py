from tradiba.strategy.governance.policy import StrategicGovernance

def test_governance():
    gov = StrategicGovernance()
    assert not gov.evaluate_proposal({"cost": 2000000})
    assert gov.evaluate_proposal({"cost": 500000})
