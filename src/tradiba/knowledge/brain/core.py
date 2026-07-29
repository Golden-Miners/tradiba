from typing import Dict, Any

class DigitalBrainCore:
    """
    Maintains a continuously evolving organizational memory.
    Stores trading knowledge, AI reasoning, research outcomes, engineering knowledge, etc.
    """
    def __init__(self):
        self.knowledge_base: Dict[str, Dict[str, Any]] = {}

    def store_knowledge(self, entity_id: str, data: Dict[str, Any]) -> None:
        self.knowledge_base[entity_id] = data

    def retrieve_knowledge(self, entity_id: str) -> Dict[str, Any]:
        return self.knowledge_base.get(entity_id, {})
