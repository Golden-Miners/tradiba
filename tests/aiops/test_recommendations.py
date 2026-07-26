from tradiba.aiops.anomaly import Anomaly
from tradiba.aiops.recommendations import RecommendationEngine

def test_recommendation_engine():
    engine = RecommendationEngine()
    
    anomalies = [
        Anomaly(type="latency_spike", severity="high", confidence=0.9, affected_components=[], evidence=""),
    ]
    
    recs = engine.generate(anomalies)
    assert len(recs) == 1
    assert recs[0].priority == "high"
    assert "secondary broker" in recs[0].action
