import json
import os
from typing import List, Dict, Any

class EpisodicMemory:
    """Stores past executions and step-by-step logs."""
    def __init__(self, storage_path: str = ".data/hermes/episodes.json"):
        self.storage_path = storage_path
        self.episodes: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                return json.load(f)
        return []

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump(self.episodes, f, indent=2)

    def log_episode(self, goal_id: str, plan: List[str], outcome: str, reflection: str):
        episode = {
            "goal_id": goal_id,
            "plan": plan,
            "outcome": outcome,
            "reflection": reflection
        }
        self.episodes.append(episode)
        self._save()
