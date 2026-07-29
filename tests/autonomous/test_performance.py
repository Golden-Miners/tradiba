from tradiba.autonomous.performance.intelligence import EnterprisePerformanceIntelligence

def test_performance():
    perf = EnterprisePerformanceIntelligence()
    assert perf.get_health_score() > 90
