from tradiba.ai.governance.platform import AIGovernancePlatform

def test_governance():
    gov = AIGovernancePlatform()
    assert gov.enforce_policy("ADMIN", "DELETE")
    assert not gov.enforce_policy("GUEST", "DELETE")
    assert gov.enforce_policy("GUEST", "READ")
    
    assert len(gov.get_audit_trail()) == 3
