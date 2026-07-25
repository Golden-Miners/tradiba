import pytest
import asyncio
from tradiba.distributed.election import LeaderElection

@pytest.mark.asyncio
async def test_leader_election():
    election = LeaderElection(node_id="node-1", resource="scheduler", ttl_seconds=2)
    
    # Start election
    await election.start()
    assert election.is_leader is True
    
    # Wait to ensure renewal task works (or at least doesn't crash)
    await asyncio.sleep(0.1)
    assert election.is_leader is True
    
    # Stop election
    await election.stop()
    assert election.is_leader is False
