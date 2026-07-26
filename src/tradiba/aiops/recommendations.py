from dataclasses import dataclass
from tradiba.aiops.anomaly import Anomaly

@dataclass
class Recommendation:
    priority: str
    rationale: str
    expected_impact: str
    confidence: float
    action: str

class RecommendationEngine:
    """Provides actionable recommendations based on anomalies and health scores."""
    def generate(self, anomalies: list[Anomaly]) -> list[Recommendation]:
        recs = []
        for anomaly in anomalies:
            if anomaly.type == "latency_spike":
                recs.append(Recommendation(
                    priority="high",
                    rationale="Broker latency is causing execution delays and potential slippage.",
                    expected_impact="Restore sub-10ms execution times.",
                    confidence=0.90,
                    action="Switch to a secondary broker."
                ))
            elif anomaly.type == "resource_exhaustion":
                recs.append(Recommendation(
                    priority="critical",
                    rationale="Node memory is nearing OOM threshold.",
                    expected_impact="Prevent platform crash.",
                    confidence=0.95,
                    action="Increase worker capacity."
                ))
        return recs
