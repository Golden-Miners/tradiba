from __future__ import annotations

from typing import Dict

from tradiba.core.service import Service
from tradiba.events import EventBus
from tradiba.logging import get_logger
from tradiba.ports.execution import ExecutionProvider
from tradiba.strategy import Direction, Signal

from tradiba.risk.events import RiskApprovedEvent
from .events import OrderFilledEvent, OrderRejectedEvent, OrderSubmittedEvent
from .models.order import Order, OrderSide, OrderType
from tradiba.ports.clock import get_clock
import uuid

logger = get_logger(__name__)


class ExecutionService(Service):
    """
    Executes trading signals via an ExecutionProvider.
    Maintains order history and publishes execution events.
    """

    def __init__(
        self,
        event_bus: EventBus,
        provider: ExecutionProvider,
    ) -> None:
        self._event_bus = event_bus
        self._provider = provider
        self._orders: Dict[str, Order] = {}

    def start(self) -> None:
        self._event_bus.subscribe(RiskApprovedEvent, self._on_approved_signal)
        logger.info("ExecutionService started.")

    def stop(self) -> None:
        self._event_bus.unsubscribe(RiskApprovedEvent, self._on_approved_signal)
        logger.info("ExecutionService stopped.")

    def _on_approved_signal(self, event: RiskApprovedEvent) -> None:
        self.execute(event.signal)

    def execute(self, signal: Signal) -> None:
        """Execute a trading signal."""
        logger.info("Executing signal: %s", signal)
        
        # Determine side and default volume (using a dummy volume for now if not provided,
        # but risk engine should provide size. We'll use 0.01 standard lots).
        volume = 0.01
        
        order_side = OrderSide.BUY if signal.direction == Direction.LONG else OrderSide.SELL
        order_type = OrderType.MARKET # We default to market execution for now
        
        order = Order(
            id=str(uuid.uuid4()),
            symbol=signal.symbol,
            side=order_side,
            order_type=order_type,
            volume=volume,
            price=signal.entry,
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
            created_at=get_clock().now(),
        )
        
        self._orders[order.id] = order
        self._event_bus.publish(OrderSubmittedEvent(order=order))
        
        try:
            if order.side == OrderSide.BUY:
                result = self._provider.buy(
                    symbol=order.symbol,
                    volume=order.volume,
                    sl=order.stop_loss,
                    tp=order.take_profit,
                )
            else:
                result = self._provider.sell(
                    symbol=order.symbol,
                    volume=order.volume,
                    sl=order.stop_loss,
                    tp=order.take_profit,
                )
                
            if result.success:
                logger.info("Order executed successfully. Ticket: %s", result.ticket)
                self._event_bus.publish(OrderFilledEvent(order=order))
            else:
                logger.warning("Order rejected by broker: %s", result.message)
                self._event_bus.publish(OrderRejectedEvent(order=order, reason=result.message))
                
        except Exception as e:
            logger.exception("Execution failed.")
            self._event_bus.publish(OrderRejectedEvent(order=order, reason=str(e)))
