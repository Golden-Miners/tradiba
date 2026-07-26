from tradiba.aiops.anomaly import Anomaly
from tradiba.aiops.recommendations import Recommendation
from tradiba.aiops.explain import ExplainabilityEngine

def test_explainability():
    engine = ExplainabilityEngine()
    
    anomaly = Anomaly(type="latency_spike", severity="high", confidence=0.9, affected_components=[], evidence="Latency 150ms")
    rec = Recommendation(priority="high", rationale="Fix it", expected_impact="Good", confidence=0.9, action="Switch broker")
    chain = "Delay -> Congestion"
    
    explanation = engine.explain(anomaly, rec, chain)
    
    rendered = explanation.render()
    assert "Observation\n↓\nlatency_spike" in rendered
    assert "Reasoning\n↓\nDelay -> Congestion" in rendered
    assert "Recommended Action\n↓\nSwitch broker" in rendered
