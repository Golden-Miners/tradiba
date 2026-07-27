import pytest
import asyncio
from tradiba.hermes.collective.runtime.environment import AgentRuntime
from tradiba.hermes.collective.agents.specialized import MarketAgent

@pytest.mark.asyncio
async def test_agent_crash_recovery():
    runtime = AgentRuntime()
    market = MarketAgent("market_1", runtime.blackboard, runtime.bus, runtime.registry)
    await runtime.register_and_start_agent(market)
    
    # Simulate a crash
    await market.stop()
    assert runtime.registry.get_agent_capabilities("market_1") == {}
    
    # Restart
    await runtime.register_and_start_agent(market)
    assert "market_1" in runtime.registry.get_all_agents()
