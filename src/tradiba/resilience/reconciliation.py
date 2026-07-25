from tradiba.events import EventBus
from tradiba.resilience.events import ReconciliationCompletedEvent
import logging

logger = logging.getLogger(__name__)

class ReconciliationEngine:
    """
    Compares internal state against external broker state to detect discrepancies.
    """
    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus

    def reconcile_positions(self, internal_positions: dict[str, float], broker_positions: dict[str, float]) -> dict[str, float]:
        """
        Returns a dictionary of symbol to quantity mismatch.
        Positive means internal has more, negative means broker has more.
        """
        discrepancies = {}
        all_symbols = set(internal_positions.keys()).union(set(broker_positions.keys()))
        
        for symbol in all_symbols:
            internal_qty = internal_positions.get(symbol, 0.0)
            broker_qty = broker_positions.get(symbol, 0.0)
            if internal_qty != broker_qty:
                discrepancies[symbol] = internal_qty - broker_qty
                
        return discrepancies

    def run_reconciliation(self, internal_positions: dict[str, float], broker_positions: dict[str, float]) -> None:
        """Runs the full reconciliation process and emits events."""
        position_mismatches = self.reconcile_positions(internal_positions, broker_positions)
        
        discrepancies_found = len(position_mismatches)
        
        if discrepancies_found > 0:
            logger.warning(f"Reconciliation found {discrepancies_found} mismatches: {position_mismatches}")
            
        self._event_bus.publish(
            ReconciliationCompletedEvent(
                discrepancies_found=discrepancies_found,
                details={"position_mismatches": discrepancies_found}
            )
        )
