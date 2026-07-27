from tradiba.hermes.hcos.governance.cognitive_governance import CognitiveGovernance

def test_governance():
    gov = CognitiveGovernance(["trade:execute", "data:read"])
    
    assert gov.evaluate_skill_execution("test", ["data:read"]) == True
    assert gov.evaluate_skill_execution("test", ["data:write"]) == False
