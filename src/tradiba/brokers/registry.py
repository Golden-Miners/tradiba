from typing import Dict, List, Optional
import logging

from tradiba.brokers.base import BrokerAdapter

logger = logging.getLogger(__name__)

class BrokerRegistry:
    def __init__(self):
        self._brokers: Dict[str, BrokerAdapter] = {}

    def register(self, name: str, adapter: BrokerAdapter) -> None:
        if name in self._brokers:
            logger.warning(f"Broker '{name}' is already registered. Overwriting.")
        self._brokers[name] = adapter
        logger.info(f"Registered broker adapter '{name}'")

    def unregister(self, name: str) -> None:
        if name in self._brokers:
            del self._brokers[name]
            logger.info(f"Unregistered broker '{name}'")

    def get(self, name: str) -> Optional[BrokerAdapter]:
        return self._brokers.get(name)

    def list(self) -> List[tuple[str, BrokerAdapter]]:
        return list(self._brokers.items())
