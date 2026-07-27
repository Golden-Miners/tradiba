from typing import Optional
from passlib.context import CryptContext
from tradiba.security.users.models import User, UserStatus
from tradiba.security.auth.jwt import JWTService
from tradiba.security.auth.sessions import SessionManager

# Using argon2 for hashing as requested (via passlib)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class AuthenticationService:
    def __init__(self, jwt_service: JWTService, session_manager: SessionManager):
        self.jwt = jwt_service
        self.session_manager = session_manager
        # In a real system, this would be injected a UserRepository
        self._mock_user_db: dict[str, User] = {}
        
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
        
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self._mock_user_db.get(username)
        if not user:
            return None
            
        if user.status != UserStatus.ACTIVE:
            return None
            
        if not self.verify_password(password, user.password_hash):
            return None
            
        return user
        
    def login(self, username: str, password: str, device_info: str, ip_address: str) -> Optional[str]:
        user = self.authenticate_user(username, password)
        if not user:
            return None
            
        # Create session
        session = self.session_manager.create_session(user.id, device_info, ip_address)
        
        # Create JWT token
        token_data = {
            "sub": user.id,
            "username": user.username,
            "session_id": session.session_id,
            "roles": [r.value for r in user.roles]
        }
        
        return self.jwt.create_access_token(token_data)
