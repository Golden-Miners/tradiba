from tradiba.tenancy.authorization import IdentityFederation

def test_authorization():
    federation = IdentityFederation()
    token = "some_mock_token"
    
    claims = federation.authenticate_token(token)
    assert "tenant_id" in claims
    assert "roles" in claims
