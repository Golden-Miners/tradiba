import asyncio
import logging
from typing import Any, Dict
from datetime import datetime

from tradiba.distributed.election import LeaderElection

logger = logging.getLogger(__name__)

class DistributedScheduler:
    """
    Schedules recurring jobs. Uses LeaderElection so only one node
    acts as the active scheduler.
    """
    def __init__(self, election: LeaderElection):
        self.election = election
        self._schedules: Dict[str, dict] = {}
        self._task: asyncio.Task | None = None
        self._is_running = False

    async def start(self) -> None:
        self._is_running = True
        await self.election.start()
        self._task = asyncio.create_task(self._run_loop())
        logger.info("Distributed Scheduler started")

    async def stop(self) -> None:
        self._is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        await self.election.stop()
        logger.info("Distributed Scheduler stopped")

    def schedule(self, job_id: str, cron: str, payload: Any) -> None:
        """Register a schedule."""
        self._schedules[job_id] = {"cron": cron, "payload": payload, "last_run": None}
        logger.info(f"Scheduled job {job_id} with cron '{cron}'")

    def cancel(self, job_id: str) -> None:
        """Cancel a schedule."""
        if job_id in self._schedules:
            del self._schedules[job_id]
            logger.info(f"Cancelled job {job_id}")

    def execute_due(self) -> None:
        """Execute jobs that are due."""
        # Only execute if we are the leader
        if not self.election.is_leader:
            return

        now = datetime.now()
        for job_id, meta in self._schedules.items():
            # In a real system, parse cron. Here we just mock it.
            # Example logic: run if last_run is None
            if meta["last_run"] is None:
                logger.info(f"[LEADER] Executing scheduled job {job_id}")
                meta["last_run"] = now
                # In real system, this would push a job to the bus/queue

    async def _run_loop(self) -> None:
        while self._is_running:
            try:
                self.execute_due()
            except Exception as e:
                logger.error(f"Error executing due jobs: {e}")
            await asyncio.sleep(1) # Check every second
