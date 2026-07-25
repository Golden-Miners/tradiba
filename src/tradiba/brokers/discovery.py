from tradiba.brokers.base import BrokerAdapter
from tradiba.strategy.models import TradingSignal
import logging

logger = logging.getLogger(__name__)

class ExecutionCapabilityNegotiator:
    """
    Adapts execution plans to broker capabilities before routing.
    """
    def __init__(self):
        pass

    def negotiate(self, adapter: BrokerAdapter, signal: TradingSignal) -> TradingSignal:
        """
        Adjusts the trading signal based on what the broker supports.
        For example, converting a complex order into simpler components
        if the broker does not natively support the original request.
        """
        caps = adapter.capabilities
        
        # Example: if limit orders are not supported, maybe fallback to market order?
        # In a real system, you might simulate limit orders client-side.
        if signal.entry > 0.0 and not caps.supports_limit_orders:
            logger.warning("Broker does not support limit orders. Rejecting or adapting signal.")
            # For now, just return the signal as-is and let the execution engine fail it
            pass

        return signal
