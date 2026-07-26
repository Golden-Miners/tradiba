import uuid
from typing import Callable
from datetime import datetime

class OperationalScheduler:
    """Schedules operational workflows."""
    def __init__(self) -> None:
        self._jobs: dict[uuid.UUID, dict] = {}
        
    def schedule_job(self, name: str, cron_expr: str, action: Callable[[], None]) -> uuid.UUID:
        job_id = uuid.uuid4()
        self._jobs[job_id] = {
            "name": name,
            "cron_expr": cron_expr,
            "action": action,
            "last_run": None
        }
        return job_id

    def run_pending(self, current_time: datetime) -> None:
        """Simulates running pending jobs."""
        for job_id, job in self._jobs.items():
            # In a real system, this would evaluate cron_expr against current_time
            job["action"]()
            job["last_run"] = current_time
