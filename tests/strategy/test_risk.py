from tradiba.strategy.risk.propagation import EnterpriseRiskPropagationEngine

def test_risk():
    engine = EnterpriseRiskPropagationEngine()
    res = engine.calculate_propagation({})
    assert len(res) == 1
    assert res[0]["affected_domain"] == "Trading"
