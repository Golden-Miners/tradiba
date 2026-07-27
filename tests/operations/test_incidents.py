from tradiba.operations.incidents import IncidentManager, IncidentSeverity, IncidentStatus

def test_report_incident():
    """Test reporting a new incident."""
    manager = IncidentManager()
    incident = manager.report_incident(
        title="API Gateway Down",
        description="All API requests failing with 502 Bad Gateway",
        severity=IncidentSeverity.SEV1,
        components=["API Gateway"]
    )
    
    assert incident.id == "INC-0001"
    assert incident.severity == IncidentSeverity.SEV1
    assert incident.status == IncidentStatus.OPEN
    assert "API Gateway" in incident.affected_components
    assert len(manager.get_active_incidents()) == 1

def test_resolve_incident():
    """Test resolving an active incident."""
    manager = IncidentManager()
    incident = manager.report_incident("DB Latency", "High query latency", IncidentSeverity.SEV2, ["Database"])
    
    updated = manager.update_status(incident.id, IncidentStatus.RESOLVED)
    assert updated is not None
    assert updated.status == IncidentStatus.RESOLVED
    assert updated.resolved_at is not None
    assert len(manager.get_active_incidents()) == 0
