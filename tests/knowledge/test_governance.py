from tradiba.knowledge.governance.knowledge_policy import KnowledgeGovernance

def test_governance():
    gov = KnowledgeGovernance()
    assert gov.evaluate_access("admin", "confidential")
    assert not gov.evaluate_access("user", "confidential")
    assert gov.evaluate_access("user", "public")
