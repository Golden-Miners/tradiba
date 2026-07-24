from typing import List
from tradiba.events import Event
from tradiba.mt5.models import Candle
from tradiba.market_structure.state import TimeframeState
from tradiba.market_structure.models import Trend, BreakOfStructure, ChangeOfCharacter
from tradiba.market_structure.events import TrendChangedEvent, BOSEvent, CHOCHEvent
from .base import Detector

class TrendDetector(Detector):
    def update(self, candle: Candle, state: TimeframeState, current_events: List[Event]) -> List[Event]:
        events = []
        
        # Initial trend establishment
        if state.trend == Trend.NEUTRAL:
            if state.last_swing_high and candle.close > state.last_swing_high.price:
                state.trend = Trend.BULLISH
                events.append(TrendChangedEvent(symbol=state.symbol, timeframe=state.timeframe, old_trend=Trend.NEUTRAL, new_trend=Trend.BULLISH))
                state.last_swing_high = None
            elif state.last_swing_low and candle.close < state.last_swing_low.price:
                state.trend = Trend.BEARISH
                events.append(TrendChangedEvent(symbol=state.symbol, timeframe=state.timeframe, old_trend=Trend.NEUTRAL, new_trend=Trend.BEARISH))
                state.last_swing_low = None
            return events

        # Upward break
        if state.last_swing_high and candle.close > state.last_swing_high.price:
            if state.trend == Trend.BULLISH:
                bos = BreakOfStructure(candle=candle, broken_price=state.last_swing_high.price, direction=Trend.BULLISH)
                state.bos_history.append(bos)
                state.last_bos = bos
                events.append(BOSEvent(symbol=state.symbol, direction=Trend.BULLISH, broken_price=bos.broken_price, candle=candle, bos=bos))
                state.last_swing_high = None
            else:
                choch = ChangeOfCharacter(candle=candle, broken_price=state.last_swing_high.price, direction=Trend.BULLISH)
                state.choch_history.append(choch)
                state.last_choch = choch
                events.append(CHOCHEvent(choch=choch))
                events.append(TrendChangedEvent(symbol=state.symbol, timeframe=state.timeframe, old_trend=state.trend, new_trend=Trend.BULLISH))
                state.trend = Trend.BULLISH
                state.last_swing_high = None
                
        # Downward break
        elif state.last_swing_low and candle.close < state.last_swing_low.price:
            if state.trend == Trend.BEARISH:
                bos = BreakOfStructure(candle=candle, broken_price=state.last_swing_low.price, direction=Trend.BEARISH)
                state.bos_history.append(bos)
                state.last_bos = bos
                events.append(BOSEvent(symbol=state.symbol, direction=Trend.BEARISH, broken_price=bos.broken_price, candle=candle, bos=bos))
                state.last_swing_low = None
            else:
                choch = ChangeOfCharacter(candle=candle, broken_price=state.last_swing_low.price, direction=Trend.BEARISH)
                state.choch_history.append(choch)
                state.last_choch = choch
                events.append(CHOCHEvent(choch=choch))
                events.append(TrendChangedEvent(symbol=state.symbol, timeframe=state.timeframe, old_trend=state.trend, new_trend=Trend.BEARISH))
                state.trend = Trend.BEARISH
                state.last_swing_low = None

        return events
