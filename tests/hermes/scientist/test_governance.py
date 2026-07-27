from tradiba.hermes.scientist.governance.scientific_governance import ScientificGovernance

def test_governance():
    gov = ScientificGovernance()
    assert gov.approve_for_production("s1", {"stat": True, "peer": True})
    assert "s1" in gov.approved_research
    
    assert not gov.approve_for_production("s2", {"stat": True, "peer": False})
