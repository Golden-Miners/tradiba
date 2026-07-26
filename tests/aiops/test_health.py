from tradiba.aiops.health import StrategyHealthEngine

def test_health_scoring():
    engine = StrategyHealthEngine()
    
    healthy_state = {
        "win_rate": 0.6,
        "errors": 0,
        "risk_violations": 0,
        "latency_ms": 5,
        "uptime_hours": 48
    }
    
    score = engine.calculate_health(healthy_state)
    assert score.risk == 1.0
    assert score.stability == 1.0
    assert score.execution == 0.95
    assert score.confidence == 0.95
    assert score.overall > 0.8
    
    degraded_state = {
        "win_rate": 0.3,
        "errors": 5,
        "risk_violations": 2,
        "latency_ms": 150,
        "uptime_hours": 12
    }
    
    score_degraded = engine.calculate_health(degraded_state)
    assert score_degraded.risk < 1.0
    assert score_degraded.stability < 1.0
    assert score_degraded.execution == 0.0
    assert score_degraded.confidence == 0.5
