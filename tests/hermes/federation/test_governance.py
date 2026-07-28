from tradiba.hermes.federation.governance.federated_governance import FederatedGovernance
from tradiba.hermes.federation.sovereignty.policy_enforcer import PolicyEnforcer

def test_governance():
    gov = FederatedGovernance()
    gov.log_action("read", "org1", "success")
    assert len(gov.get_audit_trail("org1")) == 1

def test_sovereignty():
    enf = PolicyEnforcer()
    assert enf.enforce_policy({"region": "local"}, "data_residency")
    assert not enf.enforce_policy({"region": "remote"}, "data_residency")
