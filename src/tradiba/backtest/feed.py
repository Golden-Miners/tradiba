import csv
from datetime import datetime
from typing import Iterator

from tradiba.market.events import CandleClosedEvent
from tradiba.market.models import Candle, Timeframe


class HistoricalCSVFeed:
    """Reads historical OHLCV data from a CSV file."""

    def __init__(self, filepath: str, symbol: str, timeframe: Timeframe):
        self.filepath = filepath
        self.symbol = symbol
        self.timeframe = timeframe

    def read_events(self) -> Iterator[CandleClosedEvent]:
        with open(self.filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Expected format: time, open, high, low, close, tick_volume, spread, real_volume
                try:
                    dt = datetime.fromisoformat(row["time"])
                except ValueError:
                    # Try another format if isoformat fails
                    dt = datetime.strptime(row["time"], "%Y-%m-%d %H:%M:%S")

                candle = Candle(
                    symbol=self.symbol,
                    timeframe=self.timeframe,
                    open_time=dt,
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=int(row.get("tick_volume", 0)),
                )
                yield CandleClosedEvent(candle=candle)
