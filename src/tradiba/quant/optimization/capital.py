from typing import Dict, List

class CapitalAllocationOptimizer:
    """
    Optimizes capital allocation across strategies, regions, and pools.
    """
    def allocate(self, capital: float, entities: List[str]) -> Dict[str, float]:
        alloc = capital / len(entities) if entities else 0.0
        return {entity: alloc for entity in entities}
