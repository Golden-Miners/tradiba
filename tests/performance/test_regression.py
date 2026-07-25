import pytest
from tradiba.performance.regression import PerformanceBaseline
from tradiba.performance.report import PerformanceReport
from tradiba.performance.exceptions import RegressionError

def test_regression_baseline():
    base_report = PerformanceReport(
        benchmark_name="test_bench",
        latency_summary={"avg_ms": 10.0}
    )
    baseline = PerformanceBaseline(base_report)
    
    # 5% increase should pass
    new_report_pass = PerformanceReport(
        benchmark_name="test_bench",
        latency_summary={"avg_ms": 10.5}
    )
    assert baseline.compare(new_report_pass, allowed_latency_increase_pct=10.0)
    
    # 15% increase should fail
    new_report_fail = PerformanceReport(
        benchmark_name="test_bench",
        latency_summary={"avg_ms": 11.5}
    )
    with pytest.raises(RegressionError):
        baseline.compare(new_report_fail, allowed_latency_increase_pct=10.0)
