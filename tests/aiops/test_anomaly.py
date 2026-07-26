from datetime import datetime
from tradiba.aiops.configuration import PlatformSnapshot
from tradiba.aiops.anomaly import AnomalyDetector

def test_anomaly_detection():
    detector = AnomalyDetector()
    
    snapshot = PlatformSnapshot(
        timestamp=datetime.now(),
        cluster_status="healthy",
        brokers=[],
        portfolio={},
        strategies=[],
        alerts=[],
        metrics={"broker_latency_ms": 150, "memory_pct": 50}
    )
    
    anomalies = detector.detect(snapshot)
    assert len(anomalies) == 1
    assert anomalies[0].type == "latency_spike"
    assert anomalies[0].severity == "high"
    
    snapshot_oom = PlatformSnapshot(
        timestamp=datetime.now(),
        cluster_status="healthy",
        brokers=[],
        portfolio={},
        strategies=[],
        alerts=[],
        metrics={"broker_latency_ms": 10, "memory_pct": 95}
    )
    
    anomalies_oom = detector.detect(snapshot_oom)
    assert len(anomalies_oom) == 1
    assert anomalies_oom[0].type == "resource_exhaustion"
