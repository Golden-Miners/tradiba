"""
MetaTrader 5 service.
"""

from __future__ import annotations

from tradiba.core.service import Service
from tradiba.logging import get_logger

logger = get_logger(__name__)


class MT5Service(Service):
    """
    Manages the MetaTrader 5 connection lifecycle.
    """

    def __init__(self) -> None:
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected

    def start(self) -> None:
        """
        Placeholder until the MT5 package is integrated.
        """
        logger.info("Starting MT5 service...")
        self._connected = True

    def stop(self) -> None:
        logger.info("Stopping MT5 service...")
        self._connected = False