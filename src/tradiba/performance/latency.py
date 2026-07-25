import time
from tradiba.performance.profiler import Profiler
from typing import Any

class LatencyProfiler(Profiler):
    """
    Profiles end-to-end execution latency across pipeline stages.
    """
    def __init__(self) -> None:
        self.start_times: dict[str, float] = {}
        self.latencies: dict[str, list[float]] = {}
        
    def start(self) -> None:
        pass
        
    def stop(self) -> None:
        pass
        
    def get_results(self) -> dict[str, Any]:
        results = {}
        for stage, lat_list in self.latencies.items():
            if not lat_list:
                continue
            avg = sum(lat_list) / len(lat_list)
            results[stage] = {
                "avg_ms": avg,
                "count": len(lat_list),
                "min_ms": min(lat_list),
                "max_ms": max(lat_list)
            }
        return results

    def mark_start(self, stage: str) -> None:
        self.start_times[stage] = time.perf_counter()
        
    def mark_end(self, stage: str) -> None:
        if stage in self.start_times:
            end = time.perf_counter()
            elapsed = (end - self.start_times[stage]) * 1000.0
            if stage not in self.latencies:
                self.latencies[stage] = []
            self.latencies[stage].append(elapsed)
            del self.start_times[stage]
