from typing import Dict

class KnowledgeLifecycleManager:
    """
    Manages knowledge states (Draft, Validated, Published, Referenced, Archived).
    """
    def __init__(self):
        self.states: Dict[str, str] = {}

    def set_state(self, knowledge_id: str, state: str) -> None:
        self.states[knowledge_id] = state

    def get_state(self, knowledge_id: str) -> str:
        return self.states.get(knowledge_id, "Draft")
