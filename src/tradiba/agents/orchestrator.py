from typing import Dict
from tradiba.agents.base.agent import Agent
from tradiba.agents.base.context import AgentContext
from tradiba.agents.recommendations import Recommendation

class AgentOrchestrator:
    """Routes tasks and orchestrates agent execution."""
    
    def __init__(self, agents: Dict[str, Agent]):
        self.agents = agents
        
    async def dispatch(self, agent_name: str, context: AgentContext) -> Recommendation:
        """Dispatch a context to a specific agent and return its recommendation."""
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} not found")
            
        result = await agent.execute(context)
        
        # Translate result into a recommendation
        return Recommendation(
            id=f"rec-{result.agent_name}-001",
            category=result.agent_name,
            priority="HIGH" if result.confidence > 0.8 else "MEDIUM",
            confidence=result.confidence,
            evidence=result.output.get("reasoning", "No evidence provided"),
            affected_resources=[],
            recommended_action=result.output.get("action", "HOLD"),
            requires_approval=True
        )
