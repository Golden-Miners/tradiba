from datetime import datetime, timezone

from tradiba.market.events import CandleClosedEvent
from tradiba.market.models import Candle, Timeframe
from tradiba.market_structure.events import SwingHighEvent
from tradiba.market_structure.models import SwingType
from tradiba.market_structure.service import MarketStructureService
from tradiba.events import EventBus

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

def test_integration_swing_detection():
    bus = EventBus()
    market_structure = MarketStructureService(event_bus=bus)
    bus.subscribe(CandleClosedEvent, market_structure.on_candle_closed)
    
    events = []
    def on_swing_high(e: SwingHighEvent):
        events.append(e)

    bus.subscribe(SwingHighEvent, on_swing_high)

    candles = [
        candle(1.1000, 1),
        candle(1.1010, 2),
        candle(1.1050, 3),
        candle(1.1020, 4),
        candle(1.1015, 5),
        candle(1.1010, 6),
    ]

    for c in candles:
        bus.publish(CandleClosedEvent(candle=c))

    # Exactly one event is published
    assert len(events) == 1
    
    # The emitted SwingPoint references the center candle of the five-candle window
    assert events[0].swing.price == 1.1050
    assert events[0].swing.type == SwingType.HIGH
    assert events[0].swing.candle_time == candles[2].open_time
