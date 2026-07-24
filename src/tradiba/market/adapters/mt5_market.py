from __future__ import annotations

import MetaTrader5 as mt5
from datetime import datetime, timezone

from tradiba.ports.market_data import MarketDataProvider
from tradiba.market.models import Candle, Tick, Timeframe
from tradiba.logging import get_logger

logger = get_logger(__name__)

def _timeframe_to_mt5(timeframe: Timeframe) -> int:
    mapping = {
        Timeframe.M1: mt5.TIMEFRAME_M1,
        Timeframe.M5: mt5.TIMEFRAME_M5,
        Timeframe.M15: mt5.TIMEFRAME_M15,
        Timeframe.M30: mt5.TIMEFRAME_M30,
        Timeframe.H1: mt5.TIMEFRAME_H1,
        Timeframe.H4: mt5.TIMEFRAME_H4,
        Timeframe.D1: mt5.TIMEFRAME_D1,
        Timeframe.W1: mt5.TIMEFRAME_W1,
        Timeframe.MN1: mt5.TIMEFRAME_MN1,
    }
    if timeframe not in mapping:
        raise ValueError(f"Unsupported MT5 timeframe: {timeframe}")
    return mapping[timeframe]

class MT5MarketDataAdapter(MarketDataProvider):
    """
    Implements MarketDataProvider for MetaTrader 5.
    """

    def get_tick(self, symbol: str) -> Tick:
        mt5_tick = mt5.symbol_info_tick(symbol)
        if mt5_tick is None:
            raise RuntimeError(f"Failed to get tick for {symbol}")
            
        return Tick(
            symbol=symbol,
            time=datetime.fromtimestamp(mt5_tick.time, tz=timezone.utc),
            bid=mt5_tick.bid,
            ask=mt5_tick.ask,
            volume=int(mt5_tick.volume),
        )

    def get_recent_candles(self, symbol: str, timeframe: Timeframe, count: int) -> list[Candle]:
        mt5_tf = _timeframe_to_mt5(timeframe)
        rates = mt5.copy_rates_from_pos(symbol, mt5_tf, 0, count)
        if rates is None or len(rates) == 0:
            return []
            
        return self._convert_rates_to_candles(symbol, timeframe, rates)

    def get_candles(self, symbol: str, timeframe: Timeframe, date_from: datetime, date_to: datetime) -> list[Candle]:
        mt5_tf = _timeframe_to_mt5(timeframe)
        rates = mt5.copy_rates_range(symbol, mt5_tf, date_from, date_to)
        if rates is None or len(rates) == 0:
            return []
            
        return self._convert_rates_to_candles(symbol, timeframe, rates)
        
    def _convert_rates_to_candles(self, symbol: str, timeframe: Timeframe, rates) -> list[Candle]:
        candles = []
        for rate in rates:
            dt = datetime.fromtimestamp(rate['time'], tz=timezone.utc)
            candles.append(Candle(
                symbol=symbol,
                timeframe=timeframe,
                open_time=dt,
                open=rate['open'],
                high=rate['high'],
                low=rate['low'],
                close=rate['close'],
                volume=int(rate['tick_volume'])
            ))
        return candles
