from datetime import datetime, timezone
from tradiba.market.models import Candle, Timeframe
from tradiba.market_structure.models import SwingPoint, SwingType, Trend
from tradiba.market_structure.bos import BOSDetector
from tradiba.market_structure.state import MarketStructureState
from tradiba.market_structure.events import BullishBOSEvent, BearishBOSEvent, TrendChangedEvent

def candle(price: float, t: int = 1) -> Candle:
    return Candle(
        symbol="EURUSD",
        timeframe=Timeframe.M1,
        open_time=datetime(2025, 1, 1, 12, t, 0, tzinfo=timezone.utc),
        open=price,
        high=price,
        low=price,
        close=price,
        volume=100
    )

def swing(price: float, t: SwingType) -> SwingPoint:
    c = candle(price)
    return SwingPoint(
        symbol="EURUSD",
        timeframe="M1",
        type=t,
        candle_time=c.open_time,
        price=price,
        candle=c
    )

def test_bullish_bos():
    detector = BOSDetector()
    state = MarketStructureState()
    state.last_swing_high = swing(1.1050, SwingType.HIGH)
    
    events = detector.update_candle(candle(1.1060), state)
    
    assert len(events) == 2
    assert isinstance(events[0], BullishBOSEvent)
    assert events[0].broken_price == 1.1050
    assert isinstance(events[1], TrendChangedEvent)
    assert events[1].current == Trend.BULLISH

def test_bearish_bos():
    detector = BOSDetector()
    state = MarketStructureState()
    state.last_swing_low = swing(1.0940, SwingType.LOW)
    
    events = detector.update_candle(candle(1.0935), state)
    
    assert len(events) == 2
    assert isinstance(events[0], BearishBOSEvent)
    assert events[0].broken_price == 1.0940
    assert isinstance(events[1], TrendChangedEvent)
    assert events[1].current == Trend.BEARISH

def test_no_break():
    detector = BOSDetector()
    state = MarketStructureState()
    state.last_swing_high = swing(1.1050, SwingType.HIGH)
    state.last_swing_low = swing(1.0940, SwingType.LOW)
    
    events = detector.update_candle(candle(1.1048), state)
    assert len(events) == 0

def test_trend_change():
    detector = BOSDetector()
    state = MarketStructureState()
    state.last_swing_high = swing(1.1050, SwingType.HIGH)
    
    events = detector.update_candle(candle(1.1060), state)
    
    trend_events = [e for e in events if isinstance(e, TrendChangedEvent)]
    assert len(trend_events) == 1
    assert trend_events[0].previous == Trend.UNKNOWN
    assert trend_events[0].current == Trend.BULLISH

def test_repeated_closes_above_swing_do_not_duplicate():
    detector = BOSDetector()
    state = MarketStructureState()
    state.last_swing_high = swing(1.1050, SwingType.HIGH)
    
    events1 = detector.update_candle(candle(1.1060), state)
    assert len(events1) > 0
    
    # Simulate service state update
    state.last_broken_high = state.last_swing_high.price
    state.trend = Trend.BULLISH
    
    events2 = detector.update_candle(candle(1.1070), state)
    assert len(events2) == 0
