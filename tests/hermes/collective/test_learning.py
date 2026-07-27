import pytest
from tradiba.hermes.collective.runtime.environment import AgentRuntime
from tradiba.hermes.collective.agents.specialized import LearningAgent

@pytest.mark.asyncio
async def test_learning_agent_capabilities():
    runtime = AgentRuntime()
    learner = LearningAgent("learn_1", runtime.blackboard, runtime.bus, runtime.registry)
    
    caps = learner.get_capabilities()
    assert "feedback_analysis" in caps["skills"]
