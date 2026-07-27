from tradiba.hermes.enterprise.governance.enterprise_governance import EnterpriseGovernance

def test_governance():
    gov = EnterpriseGovernance()
    assert gov.approve("d1", {"evidence": True, "executive": True})
    assert not gov.approve("d2", {"evidence": True, "executive": False})
