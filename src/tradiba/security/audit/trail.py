from datetime import datetime
from typing import Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)

class AuditLogEntry:
    def __init__(self, action: str, actor_id: str, resource: str, details: Dict[str, Any], ip_address: Optional[str] = None):
        self.timestamp = datetime.utcnow().isoformat()
        self.action = action
        self.actor_id = actor_id
        self.resource = resource
        self.details = details
        self.ip_address = ip_address

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

class AuditLogger:
    """Immutable audit trail for security-sensitive operations."""
    
    def __init__(self):
        # In production this would write to a write-only database or WORM storage
        self.logs = []
        
    def log(self, action: str, actor_id: str, resource: str, details: Dict[str, Any], ip_address: Optional[str] = None):
        entry = AuditLogEntry(action, actor_id, resource, details, ip_address)
        self.logs.append(entry)
        logger.info(f"AUDIT [{entry.action}] by {entry.actor_id} on {entry.resource}")
        
    def search(self, actor_id: Optional[str] = None, action: Optional[str] = None) -> list:
        results = self.logs
        if actor_id:
            results = [log for log in results if log.actor_id == actor_id]
        if action:
            results = [log for log in results if log.action == action]
        return results
