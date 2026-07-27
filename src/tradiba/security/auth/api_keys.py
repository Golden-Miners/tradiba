from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional
from datetime import datetime
import secrets

class ApiKeyScope(str, Enum):
    MARKET_READ = "market:read"
    ORDERS_WRITE = "orders:write"
    PORTFOLIO_READ = "portfolio:read"
    RESEARCH_RUN = "research:run"

class ApiKey(BaseModel):
    key_id: str
    secret_hash: str
    user_id: str
    name: str
    scopes: List[ApiKeyScope]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    is_active: bool = True

class ApiKeyManager:
    """Manages API Keys for service accounts and integrations."""
    
    def __init__(self):
        # Mock database of API Keys
        self.keys = {}
        
    def generate_api_key(self, user_id: str, name: str, scopes: List[ApiKeyScope], expires_at: Optional[datetime] = None):
        key_id = secrets.token_urlsafe(16)
        raw_secret = secrets.token_urlsafe(32)
        
        # In a real app we'd hash the raw_secret using Argon2 here and store the hash
        # For simplicity in this scaffold, we just store it
        api_key = ApiKey(
            key_id=key_id,
            secret_hash=raw_secret, # Should be a hash!
            user_id=user_id,
            name=name,
            scopes=scopes,
            expires_at=expires_at
        )
        self.keys[key_id] = api_key
        
        # Only time the user sees the raw secret
        return {"key_id": key_id, "secret": raw_secret}
        
    def validate_api_key(self, key_id: str, raw_secret: str, required_scope: ApiKeyScope) -> bool:
        api_key = self.keys.get(key_id)
        if not api_key:
            return False
            
        if not api_key.is_active:
            return False
            
        if api_key.expires_at and api_key.expires_at < datetime.utcnow():
            return False
            
        if required_scope not in api_key.scopes:
            return False
            
        # Should verify the hash here
        if api_key.secret_hash != raw_secret:
            return False
            
        api_key.last_used = datetime.utcnow()
        return True
