from typing import List, Optional, Dict, Any
from tradiba.hermes.models.ollama import OllamaClient
from tradiba.hermes.core.goals import HermesGoal, GoalManager, GoalStatus

# Import collective infrastructure
from tradiba.hermes.collective.runtime.environment import AgentRuntime
from tradiba.hermes.collective.supervisor.agent import SupervisorAgent

class HermesAgent:
    """
    Core entry point for the Hermes Cognitive Layer.
    Refactored in v5.1 to use the Collective Intelligence Platform where the SupervisorAgent takes over entirely.
    """
    def __init__(self, agent_id: str = "hermes-supervisor"):
        self.id = agent_id
        self.state = "idle"
        self.llm = OllamaClient(model="qwen:8b")
        self.goals = GoalManager()
        
        # Initialize Collective Runtime
        self.runtime = AgentRuntime()
        self.supervisor = SupervisorAgent(
            agent_id=self.id,
            blackboard=self.runtime.blackboard,
            bus=self.runtime.bus,
            registry=self.runtime.registry
        )
        self.current_goal: Optional[HermesGoal] = None

    async def start(self):
        await self.runtime.register_and_start_agent(self.supervisor)

    async def accept_goal(self, goal: HermesGoal):
        self.state = "planning"
        self.current_goal = goal
        self.goals.add_goal(goal)
        self.goals.update_status(goal.id, GoalStatus.IN_PROGRESS)
        
        # Post goal to blackboard for the collective
        await self.runtime.blackboard.add_active_goal({"id": goal.id, "description": goal.description})
        self.state = "executing"
        
    async def finish_goal(self, outcome: str):
        if self.current_goal:
            self.goals.update_status(self.current_goal.id, GoalStatus.COMPLETED)
            self.state = "idle"
            return f"Collective completed goal: {outcome}"
        return ""

    async def stop(self):
        await self.runtime.stop_all()
