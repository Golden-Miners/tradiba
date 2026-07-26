from tradiba.workflows.incidents import IncidentManager
from tradiba.workflows.models.incident import Incident, IncidentSeverity, IncidentStatus

def test_incident_lifecycle():
    manager = IncidentManager()
    incident = Incident(
        id="INC-01",
        severity=IncidentSeverity.HIGH,
        status=IncidentStatus.DETECTED,
        impact="API down",
        timeline=[],
        owner=None
    )
    
    manager.report_incident(incident)
    manager.acknowledge("INC-01", "alice")
    assert incident.status == IncidentStatus.ACKNOWLEDGED
    assert incident.owner == "alice"
    
    manager.mitigate("INC-01")
    assert incident.status == IncidentStatus.MITIGATED
    
    manager.resolve("INC-01")
    assert incident.status == IncidentStatus.RESOLVED
