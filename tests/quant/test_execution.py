from tradiba.quant.execution.analytics import ExecutionAnalytics

def test_execution():
    analytics = ExecutionAnalytics()
    res = analytics.analyze_execution("t1")
    assert res["fill_rate"] == 1.0
