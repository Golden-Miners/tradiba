from abc import ABC, abstractmethod
from typing import List
from tradiba.agents.base.context import AgentContext
from tradiba.agents.base.result import AgentResult

class Agent(ABC):
    """
    Base class for all AI agents.
    Agents should be stateless where practical and deterministic.
    """
    name: str
    capabilities: List[str]

    @abstractmethod
    async def execute(self, context: AgentContext) -> AgentResult:
        """Execute the agent's core logic within the provided context."""
        ...
