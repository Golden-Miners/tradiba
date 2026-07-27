import pytest
import asyncio
from tradiba.hermes.collective.supervisor.agent import SupervisorAgent
from tradiba.hermes.collective.runtime.environment import AgentRuntime
from tradiba.hermes.collective.agents.specialized import MarketAgent

@pytest.mark.asyncio
async def test_supervisor_assign_task():
    runtime = AgentRuntime()
    supervisor = SupervisorAgent("sup_1", runtime.blackboard, runtime.bus, runtime.registry)
    market = MarketAgent("market_1", runtime.blackboard, runtime.bus, runtime.registry)
    
    await runtime.register_and_start_agent(supervisor)
    await runtime.register_and_start_agent(market)
    
    # Listen to bus for task assignment
    received_msgs = []
    async def listener(msg):
        received_msgs.append(msg)
        
    await runtime.bus.subscribe("agent.market_1", listener)
    
    # Assign task
    success = await supervisor.assign_task({"id": 1, "action": "analyze"}, "market_analysis")
    assert success is True
    
    # Process bus
    await asyncio.sleep(0.01)
    
    assert len(received_msgs) == 1
    assert received_msgs[0]["payload"]["type"] == "ASSIGN_TASK"

@pytest.mark.asyncio
async def test_supervisor_assign_task_fails():
    runtime = AgentRuntime()
    supervisor = SupervisorAgent("sup_1", runtime.blackboard, runtime.bus, runtime.registry)
    await runtime.register_and_start_agent(supervisor)
    
    success = await supervisor.assign_task({"id": 1}, "missing_skill")
    assert success is False
