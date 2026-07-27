import json
import os
from typing import Dict, Any, List

class ResearchMemory:
    """Persists successful experiments and failed hypotheses to prevent duplicate work."""
    
    def __init__(self, storage_path: str = ".data/hermes/research_memory.json"):
        self.storage_path = storage_path
        self.experiments: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                return json.load(f)
        return []

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump(self.experiments, f, indent=2)

    def log_experiment(self, hypothesis_id: str, result: str, summary: str):
        self.experiments.append({
            "hypothesis_id": hypothesis_id,
            "result": result,
            "summary": summary
        })
        self._save()
