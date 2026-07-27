from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class BrokerConnectedEvent:
    broker_name: str
    status: str

class MT5ConnectionManager:
    """Mock connection manager for testing."""
    def __init__(self):
        self.connected = False

    async def connect(self) -> bool:
        self.connected = True
        return True

    async def disconnect(self) -> bool:
        self.connected = False
        return True

    @property
    def is_connected(self) -> bool:
        return self.connected
