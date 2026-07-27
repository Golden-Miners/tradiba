from enum import Enum
from typing import Set
from tradiba.security.users.models import UserRole, User

class Permission(str, Enum):
    EXECUTE_TRADES = "execute_trades"
    DEPLOY_STRATEGIES = "deploy_strategies"
    APPROVE_WORKFLOWS = "approve_workflows"
    MANAGE_BROKERS = "manage_brokers"
    MANAGE_USERS = "manage_users"
    VIEW_REPORTS = "view_reports"

# Role to Permissions mapping
ROLE_PERMISSIONS = {
    UserRole.PLATFORM_ADMIN: {
        Permission.EXECUTE_TRADES,
        Permission.DEPLOY_STRATEGIES,
        Permission.APPROVE_WORKFLOWS,
        Permission.MANAGE_BROKERS,
        Permission.MANAGE_USERS,
        Permission.VIEW_REPORTS
    },
    UserRole.TENANT_ADMIN: {
        Permission.EXECUTE_TRADES,
        Permission.DEPLOY_STRATEGIES,
        Permission.MANAGE_BROKERS,
        Permission.MANAGE_USERS,
        Permission.VIEW_REPORTS
    },
    UserRole.TRADER: {
        Permission.EXECUTE_TRADES,
        Permission.VIEW_REPORTS
    },
    UserRole.VIEWER: {
        Permission.VIEW_REPORTS
    }
}

class AuthorizationService:
    """Enforces Role-Based Access Control (RBAC)."""
    
    @staticmethod
    def get_user_permissions(user: User) -> Set[Permission]:
        permissions = set()
        for role in user.roles:
            role_perms = ROLE_PERMISSIONS.get(role, set())
            permissions.update(role_perms)
        return permissions
        
    @staticmethod
    def has_permission(user: User, permission: Permission) -> bool:
        if user.status != "active":
            return False
            
        user_permissions = AuthorizationService.get_user_permissions(user)
        return permission in user_permissions
