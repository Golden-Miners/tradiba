from tradiba.compliance.framework.engine import RegulatoryFrameworkEngine

def test_framework():
    engine = RegulatoryFrameworkEngine()
    assert engine.evaluate_rule("r1", {})
