import pytest
from tradiba.agents.strategy.agent import StrategyEvaluationAgent
from tradiba.agents.base.context import AgentContext

@pytest.mark.asyncio
async def test_strategy_agent():
    agent = StrategyEvaluationAgent()
    ctx = AgentContext({}, {}, {}, {}, {}, None, None)
    result = await agent.execute(ctx)
    
    assert result.agent_name == "strategy_evaluation"
    assert result.output["action"] == "PROMOTE_TO_PAPER"
