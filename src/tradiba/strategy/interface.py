from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from tradiba.market_structure.narrative import MarketNarrative

from .models import TradingSignal


class Strategy(ABC):

    name: str

    priority: int = 100

    enabled: bool = True

    @abstractmethod
    def evaluate(
        self,
        narrative: MarketNarrative,
    ) -> list[TradingSignal]:
        """
        Evaluate current market narrative.

        Returns zero or more signals.
        """
