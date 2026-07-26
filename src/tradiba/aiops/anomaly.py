from dataclasses import dataclass
from tradiba.aiops.configuration import PlatformSnapshot

@dataclass
class Anomaly:
    type: str
    severity: str
    confidence: float
    affected_components: list[str]
    evidence: str

class AnomalyDetector:
    """Detects operational deviations across the platform."""
    def detect(self, snapshot: PlatformSnapshot) -> list[Anomaly]:
        anomalies = []
        
        # Example naive detection based on metrics snapshot
        latency = snapshot.metrics.get("broker_latency_ms", 10)
        if latency > 100:
            anomalies.append(Anomaly(
                type="latency_spike",
                severity="high",
                confidence=0.99,
                affected_components=["broker_connection"],
                evidence=f"Latency observed at {latency}ms, exceeding 100ms threshold."
            ))
            
        memory_usage = snapshot.metrics.get("memory_pct", 0)
        if memory_usage > 90:
            anomalies.append(Anomaly(
                type="resource_exhaustion",
                severity="critical",
                confidence=0.98,
                affected_components=["trading_node_1"],
                evidence=f"Memory usage at {memory_usage}%."
            ))
            
        return anomalies
