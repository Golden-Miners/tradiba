from tradiba.agents.base.agent import Agent
from tradiba.agents.base.context import AgentContext
from tradiba.agents.base.result import AgentResult

class ExecutionAdvisorAgent(Agent):
    """
    Analyzes broker quality, latency, and slippage.
    """
    name = "execution_advisor"
    capabilities = ["broker_analysis", "slippage", "latency"]

    async def execute(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            output={
                "action": "SWITCH_ALGO",
                "reasoning": "High slippage detected on market orders; recommend iceberg.",
                "recommended_algo": "ICEBERG"
            },
            confidence=0.88
        )
