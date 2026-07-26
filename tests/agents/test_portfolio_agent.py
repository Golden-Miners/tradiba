import pytest
from tradiba.agents.portfolio.agent import PortfolioAdvisorAgent
from tradiba.agents.base.context import AgentContext

@pytest.mark.asyncio
async def test_portfolio_agent():
    agent = PortfolioAdvisorAgent()
    ctx = AgentContext({}, {}, {}, {}, {}, None, None)
    result = await agent.execute(ctx)
    
    assert result.agent_name == "portfolio_advisor"
    assert result.output["action"] == "REBALANCE"
