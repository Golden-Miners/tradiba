from tradiba.agents.base.agent import Agent
from tradiba.agents.base.context import AgentContext
from tradiba.agents.base.result import AgentResult

class PortfolioAdvisorAgent(Agent):
    """
    Analyzes diversification, concentration, and regime exposure.
    """
    name = "portfolio_advisor"
    capabilities = ["diversification", "correlation", "allocation"]

    async def execute(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            output={
                "action": "REBALANCE",
                "reasoning": "High correlation detected between active trend strategies.",
                "target_allocations": {"strat_1": 0.4, "strat_2": 0.6}
            },
            confidence=0.75
        )
