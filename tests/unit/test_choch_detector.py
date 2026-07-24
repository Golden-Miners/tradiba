from datetime import datetime, timezone
from tradiba.market.models import Candle, Timeframe
from tradiba.market_structure.models import SwingPoint, SwingType, Trend
from tradiba.market_structure.choch import CHOCHDetector
from tradiba.market_structure.state import MarketStructureState
from tradiba.market_structure.events import BullishCHOCHEvent, BearishCHOCHEvent

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

def test_bullish_trend_choch():
    state = MarketStructureState()
    state.trend = Trend.BULLISH
    state.last_swing_low = swing(1.1000, SwingType.LOW)
    
    detector = CHOCHDetector()
    events = detector.update(candle(1.0990), state)
    
    assert len(events) == 1
    assert isinstance(events[0], BearishCHOCHEvent)
    assert events[0].broken_price == 1.1000

def test_bearish_trend_choch():
    state = MarketStructureState()
    state.trend = Trend.BEARISH
    state.last_swing_high = swing(1.1050, SwingType.HIGH)
    
    detector = CHOCHDetector()
    events = detector.update(candle(1.1060), state)
    
    assert len(events) == 1
    assert isinstance(events[0], BullishCHOCHEvent)
    assert events[0].broken_price == 1.1050

def test_unknown_trend_no_choch():
    state = MarketStructureState()
    state.trend = Trend.UNKNOWN
    state.last_swing_high = swing(1.1050, SwingType.HIGH)
    state.last_swing_low = swing(1.1000, SwingType.LOW)
    
    detector = CHOCHDetector()
    events_bullish = detector.update(candle(1.1060), state)
    events_bearish = detector.update(candle(1.0990), state)
    
    assert len(events_bullish) == 0
    assert len(events_bearish) == 0

def test_duplicate_choch():
    state = MarketStructureState()
    state.trend = Trend.BULLISH
    state.last_swing_low = swing(1.1000, SwingType.LOW)
    
    detector = CHOCHDetector()
    
    # First close below emits CHOCH
    events1 = detector.update(candle(1.0990), state)
    assert len(events1) == 1
    
    # Simulate service setting state.choch_detected = True
    state.choch_detected = True
    
    # Next candle below should not emit a second CHOCH
    events2 = detector.update(candle(1.0980), state)
    assert len(events2) == 0

def test_reset_choch_after_bos():
    state = MarketStructureState()
    state.trend = Trend.BULLISH
    state.last_swing_low = swing(1.1000, SwingType.LOW)
    state.choch_detected = True
    
    detector = CHOCHDetector()
    
    # Simulate a BOS resetting the flag
    state.choch_detected = False
    
    # Next close below should now emit CHOCH
    events = detector.update(candle(1.0990), state)
    assert len(events) == 1
