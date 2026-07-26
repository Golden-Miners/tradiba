import pytest
from tradiba.autonomous_research.experiment_scheduler import ExperimentScheduler

@pytest.mark.asyncio
async def test_scheduler():
    scheduler = ExperimentScheduler()
    
    x = {"ran": False}
    def task():
        x["ran"] = True
        
    scheduler.schedule_weekly(task)
    await scheduler.run_scheduled_tasks()
    
    assert x["ran"] is True
