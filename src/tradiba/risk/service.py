from __future__ import annotations

from tradiba.core.service import Service
from tradiba.events import EventBus
from tradiba.logging import get_logger
from tradiba.strategy.events import TradingSignalCreatedEvent

from .events import TradeApprovedEvent, TradeRejectedEvent
from .models import TradePlan
from .base import RiskRule

logger = get_logger(__name__)


class RiskService(Service):

    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus
        self._rules: list[RiskRule] = []

    def add_rule(
        self,
        rule: RiskRule,
    ):
        self._rules.append(rule)

    def start(self) -> None:
        self._event_bus.subscribe(TradingSignalCreatedEvent, self._on_signal)
        logger.info("RiskService started.")

    def stop(self) -> None:
        self._event_bus.unsubscribe(TradingSignalCreatedEvent, self._on_signal)
        logger.info("RiskService stopped.")

    def _on_signal(self, event: TradingSignalCreatedEvent) -> None:
        result = self.validate(event.signal)
        
        if result.approved:
            logger.info(f"Signal approved by Risk Engine: {event.signal.symbol}")
            self._event_bus.publish(TradeApprovedEvent(signal=event.signal))
        else:
            logger.warning(f"Signal rejected by Risk Engine: {result.reason}")
            self._event_bus.publish(TradeRejectedEvent(signal=event.signal, reason=result.reason))

    def validate(
        self,
        signal: Signal,
    ) -> TradePlan:

        for rule in self._rules:
            result = rule.validate(signal)
            if not result.approved:
                return result

        return TradePlan(True)
