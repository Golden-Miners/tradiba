from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class UserStatus(str, Enum):
    ACTIVE = "active"
    LOCKED = "locked"
    DISABLED = "disabled"

class UserRole(str, Enum):
    PLATFORM_ADMIN = "platform_admin"
    TENANT_ADMIN = "tenant_admin"
    PORTFOLIO_MANAGER = "portfolio_manager"
    TRADER = "trader"
    RESEARCHER = "researcher"
    RISK_MANAGER = "risk_manager"
    VIEWER = "viewer"

class User(BaseModel):
    id: str
    username: str
    email: str
    password_hash: str
    status: UserStatus = UserStatus.ACTIVE
    roles: List[UserRole] = Field(default_factory=list)
    tenant_id: Optional[str] = None
    mfa_secret: Optional[str] = None
    mfa_enabled: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
