from tradiba.compliance.governance.workflow import RegulatoryGovernance

def test_governance():
    gov = RegulatoryGovernance()
    assert gov.review_case("c1")
