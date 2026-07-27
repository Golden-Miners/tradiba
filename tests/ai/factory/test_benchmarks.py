from tradiba.ai.factory.benchmarks.suite import BenchmarkSuite

def test_benchmarks():
    suite = BenchmarkSuite()
    res = suite.run_benchmark("v1.0", "data_v2")
    assert "overall_score" in res
