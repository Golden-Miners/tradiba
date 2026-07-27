from typing import Dict, Any

class AIFactoryRegistry:
    """
    Tracks lineage and provenance of all datasets, models, prompts, etc.
    """
    def __init__(self):
        self.artifacts: Dict[str, Dict[str, Any]] = {}
        
    def register_artifact(self, artifact_type: str, artifact_id: str, metadata: Dict[str, Any]):
        self.artifacts[f"{artifact_type}::{artifact_id}"] = metadata
        
    def get_artifact(self, artifact_type: str, artifact_id: str) -> Dict[str, Any]:
        return self.artifacts.get(f"{artifact_type}::{artifact_id}", {})
