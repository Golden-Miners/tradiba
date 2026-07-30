from tradiba.data_mesh.observability.monitor import DataObservabilityMonitor

def test_observability():
    obs = DataObservabilityMonitor()
    assert obs.check_health()
