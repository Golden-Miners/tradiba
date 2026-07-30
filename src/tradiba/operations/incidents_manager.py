from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class IncidentSeverity(str, Enum):
    SEV1 = "SEV1" # Critical outage
    SEV2 = "SEV2" # Major functionality broken
    SEV3 = "SEV3" # Minor degradation
    SEV4 = "SEV4" # Cosmetic / No impact

class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    MITIGATED = "MITIGATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class Incident(BaseModel):
    id: str
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus = IncidentStatus.OPEN
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    affected_components: List[str] = Field(default_factory=list)

class Postmortem(BaseModel):
    incident_id: str
    root_cause: str
    timeline: List[Dict[str, Any]]
    action_items: List[str]

class IncidentManager:
    """In-memory tracking for active system incidents (Mock for DB)."""
    
    def __init__(self):
        self.incidents: Dict[str, Incident] = {}
        self.postmortems: Dict[str, Postmortem] = {}

    def report_incident(self, title: str, description: str, severity: IncidentSeverity, components: List[str]) -> Incident:
        incident_id = f"INC-{len(self.incidents) + 1:04d}"
        incident = Incident(
            id=incident_id,
            title=title,
            description=description,
            severity=severity,
            affected_components=components
        )
        self.incidents[incident_id] = incident
        return incident

    def update_status(self, incident_id: str, status: IncidentStatus) -> Optional[Incident]:
        incident = self.incidents.get(incident_id)
        if not incident:
            return None
            
        incident.status = status
        if status in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED]:
            incident.resolved_at = datetime.utcnow()
            
        return incident

    def get_active_incidents(self) -> List[Incident]:
        return [inc for inc in self.incidents.values() if inc.status not in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED]]

    def create_postmortem(self, incident_id: str, root_cause: str, timeline: List[Dict[str, Any]], action_items: List[str]) -> Optional[Postmortem]:
        if incident_id not in self.incidents:
            return None
        pm = Postmortem(
            incident_id=incident_id,
            root_cause=root_cause,
            timeline=timeline,
            action_items=action_items
        )
        self.postmortems[incident_id] = pm
        return pm

    def correlate_alerts(self, alerts: List[Dict[str, Any]]) -> Optional[Incident]:
        """Simple heuristic to group similar alerts into a single incident."""
        if not alerts:
            return None
        # E.g., if multiple alerts from 'API Gateway', group them
        components = list(set(a.get("component", "unknown") for a in alerts))
        descriptions = [a.get("message", "") for a in alerts]
        return self.report_incident(
            title=f"Correlated Incident: {len(alerts)} alerts detected",
            description=" | ".join(descriptions),
            severity=IncidentSeverity.SEV2,
            components=components
        )
