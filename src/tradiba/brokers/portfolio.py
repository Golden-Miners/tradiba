from typing import List, Any
from tradiba.brokers.registry import BrokerRegistry
from decimal import Decimal

class FXConversionService:
    def convert(self, amount: Decimal, from_currency: str, to_currency: str) -> Decimal:
        """
        Convert an amount from one currency to another.
        Placeholder implementation.
        """
        if from_currency == to_currency:
            return amount
        # In a real system, we'd fetch exchange rates
        return amount

class PortfolioAggregator:
    def __init__(self, registry: BrokerRegistry, fx_service: FXConversionService):
        self.registry = registry
        self.fx_service = fx_service

    def aggregate_positions(self) -> List[Any]:
        """
        Fetch and aggregate positions across all registered brokers.
        """
        all_positions = []
        for name, adapter in self.registry.list():
            positions = adapter.positions()
            # Normalize positions and add broker tagging
            for pos in positions:
                # We assume pos is a dict or object that we can tag
                if isinstance(pos, dict):
                    pos['broker'] = name
                all_positions.append(pos)
        return all_positions
