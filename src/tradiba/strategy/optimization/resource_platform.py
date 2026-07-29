from typing import Dict

class ResourceOptimizationPlatform:
    """
    Optimizes allocation of engineering, research, AI compute, and capital.
    """
    def optimize_resources(self, resources: Dict[str, float], demands: Dict[str, float]) -> Dict[str, float]:
        return {k: min(v, demands.get(k, 0.0)) for k, v in resources.items()}
