from tradiba.security.users.models import User, UserRole
from tradiba.security.auth.sessions import SessionManager
from tradiba.security.auth.jwt import JWTService
from tradiba.security.auth.authentication import AuthenticationService

def test_login_flow():
    sessions = SessionManager()
    jwt_service = JWTService(secret_key="test_secret")
    auth_service = AuthenticationService(jwt_service, sessions)
    
    # Mock user creation
    pw_hash = auth_service.hash_password("SuperSecret123!")
    user = User(
        id="u1", 
        username="admin", 
        email="admin@tradiba.com", 
        password_hash=pw_hash,
        roles=[UserRole.PLATFORM_ADMIN]
    )
    auth_service._mock_user_db["admin"] = user
    
    # Test valid login
    token = auth_service.login("admin", "SuperSecret123!", "Web-Chrome", "192.168.1.1")
    assert token is not None
    
    # Verify token
    payload = jwt_service.verify_token(token)
    assert payload is not None
    assert payload["username"] == "admin"
    assert "platform_admin" in payload["roles"]
    
    # Verify session
    session_id = payload["session_id"]
    assert sessions.get_session(session_id) is not None
    
    # Test invalid login
    invalid = auth_service.login("admin", "WrongPass!", "Web", "1.1.1.1")
    assert invalid is None

def test_session_revocation():
    sessions = SessionManager()
    session = sessions.create_session("u1", "Mobile", "10.0.0.1")
    
    assert sessions.get_session(session.session_id) is not None
    
    sessions.revoke_session(session.session_id)
    assert sessions.get_session(session.session_id) is None
