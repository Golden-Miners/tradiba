from tradiba.security.users.models import User, UserRole
from tradiba.security.auth.authorization import AuthorizationService, Permission

def test_rbac_enforcement():
    admin = User(
        id="u1", username="admin", email="a@a.com", password_hash="h",
        roles=[UserRole.PLATFORM_ADMIN]
    )
    
    trader = User(
        id="u2", username="trader", email="t@t.com", password_hash="h",
        roles=[UserRole.TRADER]
    )
    
    # Admin checks
    assert AuthorizationService.has_permission(admin, Permission.MANAGE_USERS) is True
    assert AuthorizationService.has_permission(admin, Permission.EXECUTE_TRADES) is True
    
    # Trader checks
    assert AuthorizationService.has_permission(trader, Permission.EXECUTE_TRADES) is True
    assert AuthorizationService.has_permission(trader, Permission.MANAGE_USERS) is False
