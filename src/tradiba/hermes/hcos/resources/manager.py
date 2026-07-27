from typing import Dict

class ResourceManager:
    """
    Manages quotas for cognitive workflows.
    """
    def __init__(self, limits: Dict[str, float]):
        self.limits = limits
        self.usage: Dict[str, float] = {k: 0.0 for k in limits}
        
    def consume(self, resource: str, amount: float) -> bool:
        if resource not in self.limits:
            return True
            
        if self.usage[resource] + amount > self.limits[resource]:
            return False
            
        self.usage[resource] += amount
        return True
        
    def release(self, resource: str, amount: float):
        if resource in self.usage:
            self.usage[resource] = max(0.0, self.usage[resource] - amount)
