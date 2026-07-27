from typing import Dict, Any
import asyncio

from tradiba.hermes.collective.agents.base import BaseCollectiveAgent

class SupervisorAgent(BaseCollectiveAgent):
    """
    Manages the collective:
    - Assigns tasks
    - Balances workloads
    - Escalate unresolved conflicts
    - Produces execution plans
    """
    
    def get_capabilities(self) -> Dict[str, Any]:
        return {"skills": ["orchestration", "task_delegation", "conflict_resolution"]}
        
    async def handle_message(self, message: Dict[str, Any]):
        pass

    async def assign_task(self, task: Dict[str, Any], required_skill: str) -> bool:
        """
        Finds an agent with the required skill and assigns the task.
        """
        candidates = self.registry.find_agents_by_skill(required_skill)
        if not candidates:
            await self.bus.publish("escalation", self.id, {"reason": f"No agent found for skill: {required_skill}"})
            return False
            
        selected_agent = candidates[0] # Simple round robin/first pick
        await self.bus.publish(f"agent.{selected_agent}", self.id, {"type": "ASSIGN_TASK", "task": task})
        return True
