from dataclasses import dataclass
from datetime import datetime

@dataclass
class MaintenanceWindow:
    id: str
    description: str
    start_time: datetime
    end_time: datetime
    suspend_deployments: bool = True
    suspend_optimizations: bool = True

class MaintenanceScheduler:
    """Manages planned maintenance windows."""
    def __init__(self) -> None:
        self._windows: list[MaintenanceWindow] = []

    def schedule_window(self, window: MaintenanceWindow) -> None:
        self._windows.append(window)

    def is_maintenance_active(self, current_time: datetime) -> bool:
        return any(w.start_time <= current_time <= w.end_time for w in self._windows)
        
    def can_deploy(self, current_time: datetime) -> bool:
        for w in self._windows:
            if w.start_time <= current_time <= w.end_time and w.suspend_deployments:
                return False
        return True
