from typing import List, Dict, Any, Optional
from tradiba.hermes.models.ollama import OllamaClient
from tradiba.hermes.core.goals import HermesGoal, GoalManager, GoalStatus
from tradiba.hermes.core.planner import Planner
from tradiba.hermes.core.reflector import Reflector

class HermesAgent:
    """Core entry point for the Hermes Cognitive Layer."""
    def __init__(self, agent_id: str = "hermes-1"):
        self.id = agent_id
        self.state = "idle"
        self.llm = OllamaClient(model="qwen:8b") # Configured per user request
        
        self.goals = GoalManager()
        self.planner = Planner(self.llm)
        self.reflector = Reflector(self.llm)
        
        self.current_goal: Optional[HermesGoal] = None
        self.active_plan: List[str] = []
        self.available_tools: List[str] = ["portfolio_query", "research_query"]

    async def accept_goal(self, goal: HermesGoal):
        self.state = "planning"
        self.current_goal = goal
        self.goals.add_goal(goal)
        self.goals.update_status(goal.id, GoalStatus.IN_PROGRESS)
        
        self.active_plan = await self.planner.generate_plan(goal)
        self.state = "executing"
        # In a real system, the executor loop would take over here.
        
    async def finish_goal(self, outcome: str):
        if self.current_goal:
            reflection = await self.reflector.reflect(self.current_goal.description, outcome)
            self.goals.update_status(self.current_goal.id, GoalStatus.COMPLETED)
            self.state = "idle"
            return reflection
        return ""
