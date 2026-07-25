import os
import psutil
import threading
import time
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RuntimeDiagnostics:
    uptime: float
    active_threads: int
    memory_usage_mb: float
    cpu_usage: float
    open_positions: int
    queue_depth: int
    event_rate: float


class DiagnosticsCollector:
    """Collects runtime diagnostics."""

    def __init__(self):
        self._start_time = time.time()
        self._process = psutil.Process(os.getpid())
        
        # State placeholders for business logic injections
        self.open_positions_func = lambda: 0
        self.queue_depth_func = lambda: 0
        self.event_rate_func = lambda: 0.0

    def snapshot(self) -> RuntimeDiagnostics:
        uptime = time.time() - self._start_time
        memory_mb = self._process.memory_info().rss / (1024 * 1024)
        cpu = self._process.cpu_percent(interval=None) # Non-blocking

        return RuntimeDiagnostics(
            uptime=uptime,
            active_threads=threading.active_count(),
            memory_usage_mb=memory_mb,
            cpu_usage=cpu,
            open_positions=self.open_positions_func(),
            queue_depth=self.queue_depth_func(),
            event_rate=self.event_rate_func(),
        )
