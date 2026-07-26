import pytest
from tradiba.agents.risk.agent import RiskAdvisorAgent
from tradiba.agents.base.context import AgentContext

@pytest.mark.asyncio
async def test_risk_agent():
    agent = RiskAdvisorAgent()
    ctx = AgentContext({}, {}, {}, {}, {}, None, None)
    result = await agent.execute(ctx)
    
    assert result.agent_name == "risk_advisor"
    assert result.output["action"] == "REDUCE_EXPOSURE"
