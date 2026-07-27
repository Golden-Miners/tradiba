from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

class GoalStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class HermesGoal:
    id: str
    description: str
    priority: int = 1
    deadline: Optional[datetime] = None
    status: GoalStatus = GoalStatus.PENDING
    progress: float = 0.0
    evidence: List[str] = field(default_factory=list)

class GoalManager:
    """Manages active and historical goals for Hermes."""
    def __init__(self):
        self.goals: List[HermesGoal] = []

    def add_goal(self, goal: HermesGoal):
        self.goals.append(goal)

    def update_status(self, goal_id: str, status: GoalStatus):
        for g in self.goals:
            if g.id == goal_id:
                g.status = status
                break
