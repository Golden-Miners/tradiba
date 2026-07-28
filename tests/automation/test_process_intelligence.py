from tradiba.automation.process_intelligence.analyzer import ProcessAnalyzer

def test_process_intelligence():
    pa = ProcessAnalyzer()
    res = pa.analyze_execution({})
    assert "bottlenecks" in res
    assert pa.metrics["total_executions"] == 1
