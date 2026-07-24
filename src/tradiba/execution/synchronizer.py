from __future__ import annotations

from typing import Dict

from tradiba.core.service import Service
from tradiba.events import EventBus
from tradiba.logging import get_logger
from tradiba.ports.execution import ExecutionProvider
from tradiba.scheduler import Scheduler, Task
from tradiba.portfolio.events import PositionClosedEvent
from tradiba.strategy.models import Direction
from tradiba.execution.models.position import Position

logger = get_logger(__name__)


class ExecutionSynchronizer(Service):
    """
    Polls MT5 open positions to detect newly opened, modified, or closed positions
    that might have occurred outside of the engine's direct control.
    """

    def __init__(
        self,
        event_bus: EventBus,
        provider: ExecutionProvider,
        scheduler: Scheduler,
    ) -> None:
        self._event_bus = event_bus
        self._provider = provider
        self._scheduler = scheduler
        self._known_positions: Dict[int, Position] = {}

    def start(self) -> None:
        # Load initial positions to avoid false closes on startup
        self._sync()
        
        self._scheduler.add_task(Task(
            name="position_sync",
            interval=1.0,
            action=self._sync,
        ))
        logger.info("ExecutionSynchronizer started.")

    def stop(self) -> None:
        self._scheduler.remove_task("position_sync")
        logger.info("ExecutionSynchronizer stopped.")

    def _sync(self) -> None:
        try:
            current_positions_list = self._provider.positions()
            current_positions = {p.ticket: p for p in current_positions_list}
            
            # Detect closed positions
            closed_tickets = set(self._known_positions.keys()) - set(current_positions.keys())
            for ticket in closed_tickets:
                closed_pos = self._known_positions[ticket]
                logger.info("Detected closed position: %s", ticket)
                
                # Assuming entry/exit is just price_open for this simple model
                # MT5 History would be needed for true exit price, but we mock it as profit/loss closing price
                exit_price = closed_pos.price_open # Fallback
                
                self._event_bus.publish(PositionClosedEvent(
                    ticket=ticket,
                    symbol=closed_pos.symbol,
                    side=Direction.LONG, # TODO: determine actual side
                    volume=closed_pos.volume,
                    entry=closed_pos.price_open,
                    exit=exit_price,
                    profit=closed_pos.profit
                ))
            
            # Update known state
            self._known_positions = current_positions
        except Exception:
            logger.exception("Failed to sync positions.")
