"""
MT5 Connection Manager Service.

Handles initializing and shutting down the MT5 terminal connection.
Maintains a background reconnect loop.
"""

from __future__ import annotations

import MetaTrader5 as mt5

from tradiba.core.service import Service
from tradiba.events import EventBus, DomainEvent
from tradiba.logging import get_logger
from tradiba.scheduler import Scheduler, Task
from dataclasses import dataclass

logger = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class BrokerConnectedEvent(DomainEvent):
    """Published when the MT5 terminal connects successfully."""
    terminal_info: dict


@dataclass(frozen=True, slots=True)
class BrokerDisconnectedEvent(DomainEvent):
    """Published when the MT5 terminal disconnects."""
    reason: str


class MT5ConnectionManager(Service):
    """
    Manages the MT5 terminal connection.
    Uses a background loop to reconnect if the connection drops.
    """

    def __init__(self, event_bus: EventBus, scheduler: Scheduler, poll_interval: float = 5.0) -> None:
        self._event_bus = event_bus
        self._scheduler = scheduler
        self._poll_interval = poll_interval
        self._connected = False
        self._task_name = "mt5_connection_monitor"

    def start(self) -> None:
        """Start the connection manager and attempt to initialize MT5."""
        logger.info("Starting MT5 Connection Manager...")
        self._try_connect()
        
        self._scheduler.add_task(
            Task(
                name=self._task_name,
                interval=self._poll_interval,
                action=self._monitor_connection,
            )
        )

    def stop(self) -> None:
        """Stop the monitor and gracefully shutdown MT5."""
        self._scheduler.remove_task(self._task_name)
        if self._connected:
            mt5.shutdown()
            self._connected = False
            self._event_bus.publish(BrokerDisconnectedEvent(reason="Service stopped"))
            logger.info("MT5 shutdown successfully.")
        logger.info("MT5 Connection Manager stopped.")

    def _monitor_connection(self) -> None:
        """Scheduled task to monitor and reconnect if necessary."""
        # terminal_info() returns None if not connected
        info = mt5.terminal_info()
        
        if info is None or not info.connected:
            if self._connected:
                logger.warning("MT5 connection lost! Attempting to reconnect...")
                self._connected = False
                self._event_bus.publish(BrokerDisconnectedEvent(reason="Connection lost"))
            
            self._try_connect()
        else:
            if not self._connected:
                logger.info("MT5 reconnected successfully.")
                self._connected = True
                self._event_bus.publish(BrokerConnectedEvent(terminal_info=info._asdict()))

    def _try_connect(self) -> None:
        """Attempt to initialize MT5."""
        if not mt5.initialize():
            logger.error("MT5 initialize() failed, error code: %s", mt5.last_error())
            return
            
        info = mt5.terminal_info()
        if info and info.connected:
            self._connected = True
            logger.info("MT5 initialized successfully. Terminal: %s", info.name)
            self._event_bus.publish(BrokerConnectedEvent(terminal_info=info._asdict()))
        else:
            logger.error("MT5 initialized but terminal indicates it is not connected to broker.")
