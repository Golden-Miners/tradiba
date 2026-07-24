from datetime import datetime, timezone
from tradiba.market.models import Candle, Timeframe
from tradiba.market_structure.detector import SwingDetector
from tradiba.market_structure.models import SwingType

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

def test_detects_swing_high():
    detector = SwingDetector()
    candles = [
        candle(1.1000, 1),
        candle(1.1010, 2),
        candle(1.1050, 3),
        candle(1.1020, 4),
        candle(1.1015, 5),
    ]

    event = None
    for c in candles:
        event = detector.update(c)

    assert event is not None
    assert event.swing.type == SwingType.HIGH
    assert event.swing.price == 1.1050
    assert event.swing.candle_time == candles[2].open_time

def test_detects_swing_low():
    detector = SwingDetector()
    candles = [
        candle(1.1050, 1),
        candle(1.1010, 2),
        candle(1.0950, 3),
        candle(1.1000, 4),
        candle(1.1015, 5),
    ]

    event = None
    for c in candles:
        event = detector.update(c)

    assert event is not None
    assert event.swing.type == SwingType.LOW
    assert event.swing.price == 1.0950
    assert event.swing.candle_time == candles[2].open_time

def test_no_swing_generated():
    detector = SwingDetector()
    candles = [
        candle(1.1000, 1),
        candle(1.1010, 2),
        candle(1.1020, 3),
        candle(1.1030, 4),
        candle(1.1040, 5),
    ]

    event = None
    for c in candles:
        event = detector.update(c)

    assert event is None

def test_multiple_sequential_swings():
    detector = SwingDetector()
    candles = [
        candle(1.1000, 1),
        candle(1.1010, 2),
        candle(1.1050, 3), # Swing High
        candle(1.1010, 4),
        candle(1.0950, 5), # Swing Low (wait, needs more candles to detect)
        candle(1.1000, 6),
        candle(1.1020, 7),
    ]

    events = []
    for c in candles:
        evt = detector.update(c)
        if evt:
            events.append(evt)

    assert len(events) == 2
    assert events[0].swing.type == SwingType.HIGH
    assert events[0].swing.price == 1.1050
    assert events[1].swing.type == SwingType.LOW
    assert events[1].swing.price == 1.0950

def test_equal_highs_lows_no_swing():
    detector = SwingDetector()
    candles = [
        candle(1.1000, 1),
        candle(1.1010, 2),
        candle(1.1050, 3),
        candle(1.1050, 4), # Equal high
        candle(1.1015, 5),
    ]

    event = None
    for c in candles:
        event = detector.update(c)

    # Since c2.high > c3.high is False, no swing should be detected
    assert event is None
