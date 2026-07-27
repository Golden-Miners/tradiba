from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class UnifiedCognitiveState:
    """
    Central dataclass tracking the entire cognitive state of Hermes.
    """
    session_id: str
    active_goals: List[Dict[str, Any]] = field(default_factory=list)
    running_tasks: List[Dict[str, Any]] = field(default_factory=list)
    available_resources: Dict[str, Any] = field(default_factory=dict)
    market_context: Dict[str, Any] = field(default_factory=dict)
    portfolio_context: Dict[str, Any] = field(default_factory=dict)
    system_health: str = "HEALTHY"
    learning_progress: Dict[str, Any] = field(default_factory=dict)
    
    def update_market_context(self, update: Dict[str, Any]):
        self.market_context.update(update)

    def add_goal(self, goal: Dict[str, Any]):
        self.active_goals.append(goal)

    def remove_goal(self, goal_id: str):
        self.active_goals = [g for g in self.active_goals if g.get("id") != goal_id]
