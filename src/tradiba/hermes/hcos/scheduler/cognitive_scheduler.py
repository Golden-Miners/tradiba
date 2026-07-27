from typing import Dict, Any, List
import heapq

class CognitiveScheduler:
    """
    Prioritizes cognitive work queues based on urgency and priority.
    """
    def __init__(self):
        # Using a priority queue (min-heap) where lower number means higher priority
        self.queue: List[Any] = []
        self.counter = 0
        
    def schedule_task(self, task_id: str, priority: int, payload: Dict[str, Any]):
        heapq.heappush(self.queue, (priority, self.counter, task_id, payload))
        self.counter += 1
        
    def next_task(self) -> Dict[str, Any]:
        if not self.queue:
            return {}
        priority, _, task_id, payload = heapq.heappop(self.queue)
        return {"task_id": task_id, "priority": priority, "payload": payload}
        
    def preempt_critical(self, task_id: str, payload: Dict[str, Any]):
        """Injects a critical task with highest priority (0)."""
        self.schedule_task(task_id, 0, payload)
