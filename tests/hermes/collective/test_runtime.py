import pytest
import asyncio
from tradiba.hermes.collective.runtime.environment import AgentRuntime
from tradiba.hermes.collective.agents.specialized import MarketAgent

@pytest.mark.asyncio
async def test_agent_runtime():
    runtime = AgentRuntime()
    agent = MarketAgent("market_1", runtime.blackboard, runtime.bus, runtime.registry)
    
    await runtime.register_and_start_agent(agent)
    
    assert runtime.get_agent("market_1") == agent
    assert "market_1" in runtime.registry.get_all_agents()
    
    await runtime.stop_all()
    assert runtime.get_agent("market_1") is None
