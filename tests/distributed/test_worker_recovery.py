import pytest
import asyncio
from typing import Any
from tradiba.distributed.worker import Worker

class MockWorker(Worker):
    def __init__(self):
        super().__init__("mock")
        self.processed = 0
        self.should_crash = False

    async def _run(self) -> None:
        while self._is_running:
            if self.should_crash:
                raise RuntimeError("Simulated crash")
            await asyncio.sleep(0.01)

    async def process(self, message: Any) -> None:
        self.processed += 1

@pytest.mark.asyncio
async def test_worker_graceful_shutdown():
    worker = MockWorker()
    
    # Run in background
    task = asyncio.create_task(worker.start())
    
    # Let it run briefly
    await asyncio.sleep(0.05)
    assert worker.health()["status"] == "running"
    
    # Graceful stop
    await worker.stop()
    await task
    
    assert worker.health()["status"] == "stopped"

@pytest.mark.asyncio
async def test_worker_crash_handling():
    worker = MockWorker()
    worker.should_crash = True
    
    # Should exit cleanly despite internal crash
    await worker.start()
    
    assert worker.health()["status"] == "stopped"
