import logging
from typing import Optional, Any

from tradiba.brokers.registry import BrokerRegistry
from tradiba.brokers.discovery import ExecutionCapabilityNegotiator
from tradiba.strategy.models import TradingSignal
from tradiba.brokers.exceptions import RoutingError

logger = logging.getLogger(__name__)

class OrderRouter:
    def __init__(self, registry: BrokerRegistry, negotiator: ExecutionCapabilityNegotiator):
        self.registry = registry
        self.negotiator = negotiator

    def route(self, signal: TradingSignal, preferred_broker: Optional[str] = None) -> Any:
        """
        Routes the trading signal to the appropriate broker.
        """
        if preferred_broker:
            adapter = self.registry.get(preferred_broker)
            if adapter:
                logger.info(f"Routing to preferred broker: {preferred_broker}")
                adapted_signal = self.negotiator.negotiate(adapter, signal)
                return adapter.submit(adapted_signal)
            else:
                raise RoutingError(f"Preferred broker {preferred_broker} not found")
        
        # Simple failover routing: just pick the first available broker
        brokers = self.registry.list()
        if not brokers:
            raise RoutingError("No brokers registered for routing")
            
        broker_name, adapter = brokers[0]
        logger.info(f"Routing to default broker: {broker_name}")
        adapted_signal = self.negotiator.negotiate(adapter, signal)
        return adapter.submit(adapted_signal)
