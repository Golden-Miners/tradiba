"""
Historical data source abstractions.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator

from tradiba.mt5.models import Tick


class HistoricalDataSource(ABC):
    """
    Abstract base class for reading historical market data.
    """

    @abstractmethod
    def read_ticks(self) -> Iterator[Tick]:
        """
        Yield historical ticks in chronological order.
        """
        pass
