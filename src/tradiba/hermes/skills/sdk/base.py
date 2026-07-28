from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod

class Skill(ABC):
    """
    Standard Base SDK for building reusable Hermes Skill Packs.
    """
    def __init__(self, skill_id: str, name: str, version: str):
        self.id = skill_id
        self.name = name
        self.version = version
        self.initialized = False
        self.tools: List[str] = []
        self.policies: List[str] = []

    def initialize(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.initialized = True

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def validate(self) -> bool:
        return self.initialized and len(self.id) > 0

    def shutdown(self) -> None:
        self.initialized = False

    def register_tool(self, tool_name: str) -> None:
        if tool_name not in self.tools:
            self.tools.append(tool_name)

    def declare_policy(self, policy_name: str) -> None:
        if policy_name not in self.policies:
            self.policies.append(policy_name)
