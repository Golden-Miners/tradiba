import time
from tradiba.performance.latency import LatencyProfiler

def test_latency_profiler():
    profiler = LatencyProfiler()
    profiler.start()
    
    profiler.mark_start("stage1")
    time.sleep(0.01)
    profiler.mark_end("stage1")
    
    profiler.mark_start("stage1")
    time.sleep(0.02)
    profiler.mark_end("stage1")
    
    profiler.stop()
    
    results = profiler.get_results()
    assert "stage1" in results
    assert results["stage1"]["count"] == 2
    assert results["stage1"]["avg_ms"] > 0
    assert results["stage1"]["max_ms"] >= results["stage1"]["min_ms"]
