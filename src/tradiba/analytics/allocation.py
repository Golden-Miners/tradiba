from decimal import Decimal

class AllocationEngine:
    """
    Allocates physical capital across strategies based on target weights.
    """
    def allocate(self, strategies: list[str], target_weights: dict[str, float], total_capital: Decimal) -> dict[str, Decimal]:
        """
        Translates target percentage weights into absolute monetary allocations.
        """
        allocations = {}
        for strategy in strategies:
            weight = target_weights.get(strategy, 0.0)
            allocations[strategy] = total_capital * Decimal(str(weight))
        return allocations
