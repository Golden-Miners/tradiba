from tradiba.operations.correlation.incident_correlator import IncidentCorrelator

def test_correlation():
    corr = IncidentCorrelator()
    incidents = corr.correlate([{"event": "e1"}, {"event": "e2"}])
    assert len(incidents) == 1
    assert len(incidents[0]["events"]) == 2
