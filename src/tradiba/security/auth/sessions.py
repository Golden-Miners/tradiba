from typing import Dict, Optional
from datetime import datetime
import uuid

class Session:
    def __init__(self, user_id: str, device_info: str, ip_address: str):
        self.session_id: str = str(uuid.uuid4())
        self.user_id: str = user_id
        self.device_info: str = device_info
        self.ip_address: str = ip_address
        self.created_at: datetime = datetime.utcnow()
        self.last_activity: datetime = datetime.utcnow()
        self.is_active: bool = True

class SessionManager:
    """Manages active user sessions across the platform."""
    
    def __init__(self):
        # In memory store for now, typically backed by Redis
        self.sessions: Dict[str, Session] = {}
        
    def create_session(self, user_id: str, device_info: str, ip_address: str) -> Session:
        session = Session(user_id, device_info, ip_address)
        self.sessions[session.session_id] = session
        return session
        
    def get_session(self, session_id: str) -> Optional[Session]:
        session = self.sessions.get(session_id)
        if session and session.is_active:
            session.last_activity = datetime.utcnow()
            return session
        return None
        
    def revoke_session(self, session_id: str) -> bool:
        session = self.sessions.get(session_id)
        if session:
            session.is_active = False
            return True
        return False
        
    def revoke_all_user_sessions(self, user_id: str) -> int:
        revoked = 0
        for session in self.sessions.values():
            if session.user_id == user_id and session.is_active:
                session.is_active = False
                revoked += 1
        return revoked
