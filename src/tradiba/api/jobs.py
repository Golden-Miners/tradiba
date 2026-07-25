import uuid
import asyncio
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class JobStatus(Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class JobRecord:
    id: str
    type: str
    status: JobStatus
    progress: float
    result: Optional[dict] = None
    error: Optional[str] = None


class JobManager:
    """Manages long-running background tasks."""
    
    def __init__(self):
        self._jobs: Dict[str, JobRecord] = {}

    def submit(self, job_type: str, coro) -> str:
        job_id = str(uuid.uuid4())
        self._jobs[job_id] = JobRecord(
            id=job_id,
            type=job_type,
            status=JobStatus.QUEUED,
            progress=0.0
        )
        # Fire and forget
        asyncio.create_task(self._run_job(job_id, coro))
        return job_id

    async def _run_job(self, job_id: str, coro) -> None:
        job = self._jobs[job_id]
        job.status = JobStatus.RUNNING
        try:
            result = await coro
            job.status = JobStatus.COMPLETED
            job.progress = 100.0
            job.result = result
        except Exception as e:
            job.status = JobStatus.FAILED
            job.error = str(e)

    def get_job(self, job_id: str) -> Optional[JobRecord]:
        return self._jobs.get(job_id)

    def list_jobs(self, job_type: str = None) -> list[JobRecord]:
        if job_type:
            return [j for j in self._jobs.values() if j.type == job_type]
        return list(self._jobs.values())

    def cancel(self, job_id: str) -> bool:
        # True cancellation is complex depending on the runner.
        # This is a stub that removes it from tracking if queued.
        job = self._jobs.get(job_id)
        if job and job.status == JobStatus.QUEUED:
            job.status = JobStatus.FAILED
            job.error = "Cancelled by user"
            return True
        return False


# Global instance for the FastAPI app to use
job_manager = JobManager()
