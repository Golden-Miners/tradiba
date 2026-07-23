from __future__ import annotations

from abc import ABC, abstractmethod

import typing

if typing.TYPE_CHECKING:
    from tradiba.mt5.models import Candle, Tick
    from tradiba.mt5.timeframes import Timeframe


class MarketDataProvider(ABC):

    @abstractmethod
    def get_tick(
        self,
        symbol: str,
    ) -> Tick:
        ...

    @abstractmethod
    def get_recent_candles(
        self,
        symbol: str,
        timeframe: Timeframe,
        count: int,
    ) -> list[Candle]:
        ...

    @abstractmethod
    def get_candles(
        self,
        symbol: str,
        timeframe: Timeframe,
        date_from,
        date_to,
    ) -> list[Candle]:
        ...
