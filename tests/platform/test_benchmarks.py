from tradiba.platform.benchmark.profiler import BenchmarkProfiler

def test_benchmark():
    prof = BenchmarkProfiler()
    assert prof.profile()
