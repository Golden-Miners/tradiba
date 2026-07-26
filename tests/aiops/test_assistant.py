from datetime import datetime
from tradiba.aiops.configuration import PlatformSnapshot
from tradiba.aiops.assistant import OperationalAssistant

def test_assistant_queries():
    snapshot = PlatformSnapshot(
        timestamp=datetime.now(),
        cluster_status="healthy",
        brokers=[],
        portfolio={},
        strategies=[{"id": "strat_alpha", "risk_violations": 1}],
        alerts=[],
        metrics={}
    )
    
    assistant = OperationalAssistant(snapshot)
    
    ans_latency = assistant.query("Why did execution latency increase today?")
    assert "network congestion" in ans_latency.lower()
    
    ans_risk = assistant.query("Which strategies exceeded risk limits this week?")
    assert "strat_alpha" in ans_risk
    
    ans_summary = assistant.query("Summarize overnight trading.")
    assert "exposure decreased" in ans_summary.lower()
    
    ans_quality = assistant.query("Show brokers with declining fill quality.")
    assert "Primary-FX" in ans_quality
