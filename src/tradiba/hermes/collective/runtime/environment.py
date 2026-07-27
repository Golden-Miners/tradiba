from typing import Dict

from tradiba.hermes.collective.agents.base import BaseCollectiveAgent
from tradiba.hermes.collective.blackboard.memory import BlackboardMemory
from tradiba.hermes.collective.communication.bus import CommunicationBus
from tradiba.hermes.collective.registry.capabilities import CapabilityRegistry

class AgentRuntime:
    """
    Manages the lifecycle of collective agents.
    """
    def __init__(self):
        self.blackboard = BlackboardMemory()
        self.bus = CommunicationBus()
        self.registry = CapabilityRegistry()
        self.agents: Dict[str, BaseCollectiveAgent] = {}
        
    async def register_and_start_agent(self, agent: BaseCollectiveAgent):
        self.agents[agent.id] = agent
        await agent.start()
        
    async def stop_all(self):
        for agent in self.agents.values():
            await agent.stop()
        self.agents.clear()
        
    def get_agent(self, agent_id: str) -> BaseCollectiveAgent | None:
        return self.agents.get(agent_id)
