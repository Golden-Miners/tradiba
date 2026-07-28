from tradiba.ecosystem.governance.ecosystem_policy import EcosystemGovernance

def test_governance():
    eg = EcosystemGovernance()
    assert not eg.check_compliance("app1", "network_access")
    assert eg.check_compliance("app1", "read_db")
