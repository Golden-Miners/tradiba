from typing import Callable, List
import asyncio

class ExperimentScheduler:
    """Schedules recurring autonomous research tasks."""
    
    def __init__(self):
        self.tasks: List[Callable] = []
        
    def schedule_weekly(self, task: Callable):
        self.tasks.append(task)
        
    async def run_scheduled_tasks(self):
        """Executes the scheduled research loops."""
        for task in self.tasks:
            # A real implementation would check a chron/timer before executing
            await asyncio.to_thread(task)
