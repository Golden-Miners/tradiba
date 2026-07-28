from tradiba.hermes.federation.identity.federated_identity import FederatedIdentity
from tradiba.hermes.federation.trust.trust_manager import TrustManager

def test_identity():
    ident = FederatedIdentity("org1", "node1")
    ident.register_certificate("org2", "cert_xyz")
    assert ident.get_identity()["org_id"] == "org1"

def test_trust():
    tm = TrustManager()
    assert tm.establish_trust("org2", {"allowed_actions": ["read"]})
    assert tm.evaluate_request("org2", "read")
    assert not tm.evaluate_request("org2", "write")
    assert tm.revoke_trust("org2")
