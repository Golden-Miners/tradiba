import uuid
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ResearchTopic:
    id: str
    description: str
    priority: int
    status: str = "pending"

class ResearchPlanner:
    """Schedules and prioritizes autonomous research topics for Hermes."""
    
    def __init__(self):
        self.backlog: List[ResearchTopic] = []

    def identify_weaknesses(self, performance_data: Dict[str, Any]):
        """Analyzes performance metrics to identify areas needing research."""
        # Mock logic for identifying weak strategies
        if performance_data.get("max_drawdown", 0) > 5.0:
            self.backlog.append(ResearchTopic(
                id=str(uuid.uuid4()),
                description="Investigate high drawdown periods and propose risk mitigation.",
                priority=1
            ))

    def get_next_topic(self) -> ResearchTopic | None:
        if not self.backlog:
            return None
        self.backlog.sort(key=lambda t: t.priority)
        topic = self.backlog.pop(0)
        topic.status = "in_progress"
        return topic
