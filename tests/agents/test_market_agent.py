import pytest
from tradiba.agents.market.agent import MarketIntelligenceAgent
from tradiba.agents.base.context import AgentContext

@pytest.mark.asyncio
async def test_market_agent():
    agent = MarketIntelligenceAgent()
    ctx = AgentContext({}, {}, {}, {}, {}, None, None)
    result = await agent.execute(ctx)
    
    assert result.agent_name == "market_intelligence"
    assert result.status == "SUCCESS"
    assert result.output["regime"] == "TRENDING_UP"
