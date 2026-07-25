import pytest
from tradiba.distributed.scheduler import DistributedScheduler
from tradiba.distributed.election import LeaderElection

@pytest.mark.asyncio
async def test_scheduler_lifecycle():
    election = LeaderElection(node_id="node-1", resource="scheduler", ttl_seconds=2)
    scheduler = DistributedScheduler(election)
    
    await scheduler.start()
    assert election.is_leader is True
    
    scheduler.schedule("job-1", "* * * * *", {"task": "test"})
    assert "job-1" in scheduler._schedules
    
    scheduler.cancel("job-1")
    assert "job-1" not in scheduler._schedules
    
    await scheduler.stop()
    assert election.is_leader is False
