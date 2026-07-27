from abc import ABC, abstractmethod
from typing import Dict, Any

from tradiba.hermes.collective.blackboard.memory import BlackboardMemory
from tradiba.hermes.collective.communication.bus import CommunicationBus
from tradiba.hermes.collective.registry.capabilities import CapabilityRegistry

class BaseCollectiveAgent(ABC):
    """
    Base class for all agents in the Collective Intelligence Platform.
    """
    def __init__(self, agent_id: str, blackboard: BlackboardMemory, bus: CommunicationBus, registry: CapabilityRegistry):
        self.id = agent_id
        self.blackboard = blackboard
        self.bus = bus
        self.registry = registry
        self._running = False
        
    async def start(self):
        self.registry.register_agent(self.id, self.get_capabilities())
        await self.bus.subscribe(f"agent.{self.id}", self.handle_message)
        await self.bus.subscribe("broadcast.*", self.handle_message)
        self._running = True
        
    async def stop(self):
        self.registry.unregister_agent(self.id)
        self._running = False

    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def handle_message(self, message: Dict[str, Any]):
        pass
