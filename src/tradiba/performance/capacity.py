from typing import Callable, Any
from tradiba.performance.configuration import CapacityConfig
from tradiba.performance.exceptions import CapacityExceededError
import time
import logging

logger = logging.getLogger(__name__)

class CapacityTester:
    """
    Automated load generation to verify system capacity.
    """
    def __init__(self, config: CapacityConfig):
        self.config = config

    def run_load_test(self, name: str, operation: Callable[..., Any], duration_seconds: float = 5.0) -> dict[str, float]:
        """
        Runs the operation repeatedly, measuring throughput and verifying against capacity config.
        """
        logger.info(f"Starting load test '{name}' for {duration_seconds}s...")
        
        start_time = time.perf_counter()
        end_time = start_time + duration_seconds
        
        operations_completed = 0
        latencies = []
        
        while time.perf_counter() < end_time:
            op_start = time.perf_counter()
            operation()
            op_end = time.perf_counter()
            
            latencies.append((op_end - op_start) * 1000.0)
            operations_completed += 1
            
        actual_duration = time.perf_counter() - start_time
        tps = operations_completed / actual_duration if actual_duration > 0 else 0
        
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        
        logger.info(f"Load test '{name}' completed. TPS: {tps:.2f}, Avg Latency: {avg_latency:.2f}ms")
        
        if tps < self.config.target_throughput_tps:
            raise CapacityExceededError(f"Target throughput of {self.config.target_throughput_tps} TPS not met. Actual: {tps:.2f} TPS")
            
        if avg_latency > self.config.max_latency_ms:
            raise CapacityExceededError(f"Target max latency of {self.config.max_latency_ms}ms exceeded. Actual: {avg_latency:.2f}ms")
            
        return {
            "tps": tps,
            "avg_latency_ms": avg_latency,
            "total_operations": operations_completed
        }
