import pytest
from tradiba.agents.execution.agent import ExecutionAdvisorAgent
from tradiba.agents.base.context import AgentContext

@pytest.mark.asyncio
async def test_execution_agent():
    agent = ExecutionAdvisorAgent()
    ctx = AgentContext({}, {}, {}, {}, {}, None, None)
    result = await agent.execute(ctx)
    
    assert result.agent_name == "execution_advisor"
    assert result.output["action"] == "SWITCH_ALGO"
