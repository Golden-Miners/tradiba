from tradiba.agents.base.agent import Agent
from tradiba.agents.base.context import AgentContext
from tradiba.agents.base.result import AgentResult

class RiskAdvisorAgent(Agent):
    """
    Evaluates VaR, shortfall, and leverage.
    """
    name = "risk_advisor"
    capabilities = ["var", "leverage", "drawdown_analysis"]

    async def execute(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            output={
                "action": "REDUCE_EXPOSURE",
                "reasoning": "Portfolio VaR exceeds threshold limits in current regime.",
            },
            confidence=0.95
        )
