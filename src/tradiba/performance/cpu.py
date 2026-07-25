import time
from typing import Any
from tradiba.performance.profiler import Profiler

class CpuProfiler(Profiler):
    """
    Profiles CPU time utilization. Note: Does not track true percentage across all cores,
    but tracks CPU time vs Wall time for the current process.
    """
    def __init__(self) -> None:
        self.started = False
        self.start_wall = 0.0
        self.start_cpu = 0.0
        self.end_wall = 0.0
        self.end_cpu = 0.0
        
    def start(self) -> None:
        if not self.started:
            self.start_wall = time.perf_counter()
            self.start_cpu = time.process_time()
            self.started = True
            
    def stop(self) -> None:
        if self.started:
            self.end_wall = time.perf_counter()
            self.end_cpu = time.process_time()
            self.started = False
            
    def get_results(self) -> dict[str, Any]:
        if self.started:
            return {}
            
        wall_elapsed = self.end_wall - self.start_wall
        cpu_elapsed = self.end_cpu - self.start_cpu
        
        return {
            "wall_time_s": wall_elapsed,
            "cpu_time_s": cpu_elapsed,
            "utilization": (cpu_elapsed / wall_elapsed) if wall_elapsed > 0 else 0.0
        }
