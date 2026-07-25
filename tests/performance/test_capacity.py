import pytest
import time
from tradiba.performance.capacity import CapacityTester
from tradiba.performance.configuration import CapacityConfig
from tradiba.performance.exceptions import CapacityExceededError

def test_capacity_tester_success():
    config = CapacityConfig(target_throughput_tps=10, max_latency_ms=100.0)
    tester = CapacityTester(config)
    
    def fast_op():
        pass
        
    result = tester.run_load_test("fast_op", fast_op, duration_seconds=0.2)
    assert result["tps"] >= 10
    assert result["avg_latency_ms"] <= 100.0

def test_capacity_tester_failure():
    config = CapacityConfig(target_throughput_tps=1000, max_latency_ms=1.0)
    tester = CapacityTester(config)
    
    def slow_op():
        time.sleep(0.01)
        
    with pytest.raises(CapacityExceededError):
        tester.run_load_test("slow_op", slow_op, duration_seconds=0.2)
