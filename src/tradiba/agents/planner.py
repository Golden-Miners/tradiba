from typing import List
from tradiba.agents.base.context import AgentContext
from tradiba.agents.orchestrator import AgentOrchestrator
from tradiba.agents.recommendations import Recommendation

class Planner:
    """Coordinates sequential multi-agent workflows."""
    
    def __init__(self, orchestrator: AgentOrchestrator):
        self.orchestrator = orchestrator
        
    async def run_workflow(self, workflow_sequence: List[str], context: AgentContext) -> List[Recommendation]:
        """Runs a sequence of agents and collects their recommendations."""
        recommendations = []
        for agent_name in workflow_sequence:
            rec = await self.orchestrator.dispatch(agent_name, context)
            recommendations.append(rec)
            
            # In a real system, we might update the context based on the recommendation
            # before passing it to the next agent.
            
        return recommendations
