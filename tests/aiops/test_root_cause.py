from datetime import datetime
from tradiba.aiops.configuration import PlatformSnapshot
from tradiba.aiops.anomaly import Anomaly
from tradiba.aiops.root_cause import RootCauseAnalyzer

def test_root_cause_analysis():
    rca = RootCauseAnalyzer()
    
    snapshot = PlatformSnapshot(
        timestamp=datetime.now(),
        cluster_status="healthy",
        brokers=[],
        portfolio={},
        strategies=[],
        alerts=[],
        metrics={}
    )
    
    anomalies = [
        Anomaly(type="latency_spike", severity="high", confidence=0.9, affected_components=[], evidence=""),
        Anomaly(type="resource_exhaustion", severity="high", confidence=0.9, affected_components=[], evidence="")
    ]
    
    chains = rca.analyze(snapshot, anomalies)
    assert len(chains) == 2
    assert "Network congestion" in chains[0]
    assert "Memory leak" in chains[1]
