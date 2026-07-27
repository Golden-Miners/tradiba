from typing import Dict, Any

class ModelPlatform:
    """
    Model management for multiple providers, health monitoring, tracking, and fallbacks.
    """
    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}
        
    def register_model(self, model_id: str, provider: str, cost_per_1k: float):
        self.registry[model_id] = {
            "provider": provider,
            "cost_per_1k": cost_per_1k,
            "status": "HEALTHY",
            "usage": 0
        }
        
    def get_model(self, model_id: str) -> Dict[str, Any]:
        return self.registry.get(model_id, {})
        
    def record_usage(self, model_id: str, tokens: int):
        if model_id in self.registry:
            self.registry[model_id]["usage"] += tokens
