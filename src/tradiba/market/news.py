from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List
from enum import Enum, auto

class Impact(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

@dataclass(slots=True)
class NewsEvent:
    id: str
    symbol: str # Currency (e.g., USD, EUR) or asset symbol
    title: str
    timestamp: datetime
    impact: Impact
    actual: str = ""
    forecast: str = ""
    previous: str = ""

class NewsProvider(ABC):
    """
    Abstract base class for economic calendar integrations.
    """
    @abstractmethod
    def upcoming_events(self, symbol: str) -> List[NewsEvent]:
        """
        Fetch upcoming news events relevant to the given symbol/currency.
        """
        pass
