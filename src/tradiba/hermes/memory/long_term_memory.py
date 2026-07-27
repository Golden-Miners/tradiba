import json
import os
from typing import Dict, Any

class LongTermMemory:
    """Stores accumulated experience such as user preferences and research results."""
    def __init__(self, storage_path: str = ".data/hermes/ltm.json"):
        self.storage_path = storage_path
        self.knowledge: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                return json.load(f)
        return {"preferences": {}, "research": []}

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump(self.knowledge, f, indent=2)

    def set_preference(self, key: str, value: Any):
        self.knowledge["preferences"][key] = value
        self._save()

    def archive_research(self, topic: str, report: str):
        self.knowledge["research"].append({"topic": topic, "report": report})
        self._save()
