from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class ChangeRecord(BaseModel):
    id: str
    service: str
    version: str
    change_type: str # e.g., 'deployment', 'config', 'schema_migration', 'feature_flag'
    approver: str
    related_incident_id: Optional[str] = None
    linked_adr: Optional[str] = None
    status: str = "pending" # pending, successful, failed, rolled_back
    timestamp: float = Field(default_factory=datetime.utcnow().timestamp)

class ReleaseManager:
    """Tracks and governs enterprise changes, releases, and feature flags."""
    
    def __init__(self):
        self.changes: Dict[str, ChangeRecord] = {}

    def record_change(self, service: str, version: str, change_type: str, approver: str, incident_id: Optional[str] = None, adr: Optional[str] = None) -> ChangeRecord:
        change_id = f"CHG-{len(self.changes) + 1:05d}"
        change = ChangeRecord(
            id=change_id,
            service=service,
            version=version,
            change_type=change_type,
            approver=approver,
            related_incident_id=incident_id,
            linked_adr=adr
        )
        self.changes[change_id] = change
        return change

    def update_status(self, change_id: str, status: str) -> Optional[ChangeRecord]:
        if change_id in self.changes:
            self.changes[change_id].status = status
            return self.changes[change_id]
        return None

    def get_recent_changes(self, service: Optional[str] = None, limit: int = 50) -> List[ChangeRecord]:
        results = list(self.changes.values())
        if service:
            results = [c for c in results if c.service == service]
        results.sort(key=lambda x: x.timestamp, reverse=True)
        return results[:limit]
