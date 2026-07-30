from tradiba.data_mesh.governance.federated import FederatedGovernance

def test_governance():
    gov = FederatedGovernance()
    assert gov.check_access("u1", "p1")
