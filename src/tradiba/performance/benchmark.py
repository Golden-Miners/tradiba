import time
from typing import Callable, Any
from tradiba.performance.configuration import BenchmarkConfig
from tradiba.performance.report import PerformanceReport
import statistics

class Benchmark:
    """
    Framework for repeatable performance measurements.
    """
    def __init__(self, name: str, config: BenchmarkConfig):
        self.name = name
        self.config = config

    def run(self, operation: Callable[..., Any], *args: Any, **kwargs: Any) -> PerformanceReport:
        """
        Runs the benchmark, performing warmups and recording iterations.
        """
        # Warmup
        for _ in range(self.config.warmup_iterations):
            operation(*args, **kwargs)
            
        latencies: list[float] = []
        for _ in range(self.config.iterations):
            start = time.perf_counter()
            operation(*args, **kwargs)
            end = time.perf_counter()
            latencies.append((end - start) * 1000.0) # ms
            
        avg_latency = sum(latencies) / len(latencies)
        median_latency = statistics.median(latencies)
        p95_latency = statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 2 else avg_latency
        
        latency_summary = {
            "avg_ms": avg_latency,
            "median_ms": median_latency,
            "p95_ms": p95_latency,
            "min_ms": min(latencies),
            "max_ms": max(latencies)
        }
        
        return PerformanceReport(
            benchmark_name=self.name,
            latency_summary=latency_summary,
            metadata={"iterations": self.config.iterations}
        )
