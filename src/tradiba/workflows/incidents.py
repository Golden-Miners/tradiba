from tradiba.workflows.models.incident import Incident, IncidentStatus

class IncidentManager:
    """Manages the lifecycle of operational incidents."""
    
    def __init__(self) -> None:
        self._incidents: dict[str, Incident] = {}
        
    def report_incident(self, incident: Incident) -> None:
        self._incidents[incident.id] = incident
        
    def acknowledge(self, incident_id: str, owner: str) -> None:
        incident = self._incidents.get(incident_id)
        if incident and incident.status == IncidentStatus.DETECTED:
            incident.status = IncidentStatus.ACKNOWLEDGED
            incident.owner = owner
            
    def mitigate(self, incident_id: str) -> None:
        incident = self._incidents.get(incident_id)
        if incident and incident.status in [IncidentStatus.ACKNOWLEDGED, IncidentStatus.INVESTIGATING]:
            incident.status = IncidentStatus.MITIGATED

    def resolve(self, incident_id: str) -> None:
        incident = self._incidents.get(incident_id)
        if incident:
            incident.status = IncidentStatus.RESOLVED
