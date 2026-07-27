from __future__ import annotations

from datetime import datetime, timezone

from tradiba.core.service import Service
from tradiba.logging import get_logger
from tradiba.ports.market_data import MarketDataProvider

from .client import MT5Client
from .exceptions import MT5Error
from .models import Candle, Tick
from .timeframes import Timeframe

logger = get_logger(__name__)


class MT5Service(
    Service,
    MarketDataProvider,
):

    def __init__(self) -> None:
        self.client = MT5Client()
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected

    def start(self) -> None:
        logger.info("Connecting to MT5...")
        self.client.connect()
        self._connected = True
        logger.info("MT5 connected.")

    def stop(self) -> None:
        self.client.disconnect()
        self._connected = False
        logger.info("MT5 disconnected.")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_candles(
        self,
        symbol: str,
        timeframe: Timeframe,
        date_from: datetime,
        date_to: datetime,
    ) -> list[Candle]:
        """Return candles for *symbol* between *date_from* and *date_to*."""
        rates = self.client.copy_rates_range(
            symbol,
            timeframe.value,
            date_from,
            date_to,
        )
        return self._build_candles(symbol, timeframe, rates)

    def get_tick(self, symbol: str) -> Tick:
        """Return the latest tick for *symbol*."""
        raw = self.client.symbol_info_tick(symbol)
        return Tick(
            symbol=symbol,
            timestamp=datetime.fromtimestamp(raw.time, tz=timezone.utc),
            bid=float(raw.bid),
            ask=float(raw.ask),
            last=float(raw.last),
            volume=int(raw.volume),
        )

    def get_recent_candles(
        self,
        symbol: str,
        timeframe: Timeframe,
        count: int,
    ) -> list[Candle]:
        """Return the last *count* candles for *symbol*."""
        rates = self.client.copy_rates_from_pos(
            symbol,
            timeframe.value,
            start_pos=0,
            count=count,
        )
        return self._build_candles(symbol, timeframe, rates)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_candles(
        self,
        symbol: str,
        timeframe: Timeframe,
        rates,
    ) -> list[Candle]:
        """Validate, convert, sort and return a list of :class:`Candle`."""
        if len(rates) == 0:
            return []

        candles: list[Candle] = []

        for row in rates:
            if row["high"] < row["low"]:
                raise MT5Error("Invalid candle: high < low")

            if row["high"] < max(row["open"], row["close"]):
                raise MT5Error("Invalid candle: high below open/close")

            if row["low"] > min(row["open"], row["close"]):
                raise MT5Error("Invalid candle: low above open/close")

            candles.append(
                Candle(
                    symbol=symbol,
                    timeframe=timeframe.name,
                    timestamp=datetime.fromtimestamp(
                        row["time"],
                        tz=timezone.utc,
                    ),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    tick_volume=int(row["tick_volume"]),
                    spread=int(row["spread"]),
                    real_volume=int(row["real_volume"]),
                )
            )

        candles.sort(key=lambda candle: candle.timestamp)

        for previous, current in zip(candles, candles[1:]):
            if current.timestamp <= previous.timestamp:
                raise MT5Error("Candles are not in chronological order")

        return candles