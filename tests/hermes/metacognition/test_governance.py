from tradiba.hermes.metacognition.governance.ai_governance import AIGovernanceExtensions

def test_governance():
    gov = AIGovernanceExtensions()
    gov.log_optimization("workflow", {"id": "1"})
    
    trail = gov.get_audit_trail("workflow")
    assert len(trail) == 1
    assert trail[0]["status"] == "APPROVED"
