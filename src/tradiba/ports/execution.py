from __future__ import annotations

from abc import ABC, abstractmethod

from tradiba.execution.models.result import TradeResult


class ExecutionProvider(ABC):

    @abstractmethod
    def buy(
        self,
        *,
        symbol: str,
        volume: float,
        sl: float,
        tp: float,
    ) -> TradeResult:
        ...

    @abstractmethod
    def sell(
        self,
        *,
        symbol: str,
        volume: float,
        sl: float,
        tp: float,
    ) -> TradeResult:
        ...

    @abstractmethod
    def account_info(self):
        ...

    @abstractmethod
    def positions(self):
        ...
