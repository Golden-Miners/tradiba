from __future__ import annotations

from abc import ABC, abstractmethod


class ExecutionProvider(ABC):

    @abstractmethod
    def buy(
        self,
        *,
        symbol: str,
        volume: float,
        sl: float,
        tp: float,
    ):
        ...

    @abstractmethod
    def sell(
        self,
        *,
        symbol: str,
        volume: float,
        sl: float,
        tp: float,
    ):
        ...
