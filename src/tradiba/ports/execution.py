from __future__ import annotations

from abc import ABC, abstractmethod

from tradiba.execution.models.result import TradeResult


class ExecutionProvider(ABC):

    @abstractmethod
    def buy_market(
        self,
        *,
        symbol: str,
        volume: float,
        sl: float,
        tp: float,
    ) -> TradeResult:
        ...

    @abstractmethod
    def sell_market(
        self,
        *,
        symbol: str,
        volume: float,
        sl: float,
        tp: float,
    ) -> TradeResult:
        ...

    @abstractmethod
    def close_position(self, ticket: int) -> TradeResult:
        ...

    @abstractmethod
    def modify_position(self, ticket: int, sl: float, tp: float) -> TradeResult:
        ...

    @abstractmethod
    def orders(self):
        ...

    @abstractmethod
    def account_info(self):
        ...

    @abstractmethod
    def positions(self):
        ...
