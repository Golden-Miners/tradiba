from tradiba.hermes.platform.governance.unified import UnifiedGovernance

def test_governance():
    gov = UnifiedGovernance()
    gov.add_policy("p1", {"strict": True})
    assert gov.check_compliance("action", {})
