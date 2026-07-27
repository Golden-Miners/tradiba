from tradiba.hermes.innovation.governance.promotion import InnovationGovernance

def test_governance():
    gov = InnovationGovernance()
    gov.submit_for_review("prop1", "SKILL")
    
    assert not gov.is_promotable("prop1")
    
    gov.human_approve("prop1")
    assert gov.is_promotable("prop1")
