from datetime import datetime, timezone
from tradiba.events import EventBus
from tradiba.mt5.models import Candle
from tradiba.market_structure.service import MarketStructureService
from tradiba.market_structure.events import (
    SwingHighEvent, SwingLowEvent, TrendChangedEvent,
    BOSEvent, CHOCHEvent, LiquidityCreatedEvent,
    FairValueGapCreatedEvent, OrderBlockCreatedEvent
)

def make_candle(high: float, low: float, close: float, open_: float, timestamp: int) -> Candle:
    return Candle(
        symbol="EURUSD",
        timeframe="H1",
        timestamp=datetime.fromtimestamp(timestamp, tz=timezone.utc),
        open=open_,
        high=high,
        low=low,
        close=close,
        tick_volume=100,
        real_volume=0,
        spread=1
    )

def test_smc_engine_flow():
    bus = EventBus()
    svc = MarketStructureService(bus)
    svc.start()

    events_captured = []
    
    # We want to capture events but EventBus doesn't have a catch-all
    # so we'll subscribe to all SMC events
    for event_type in [
        SwingHighEvent, SwingLowEvent, TrendChangedEvent,
        BOSEvent, CHOCHEvent, LiquidityCreatedEvent,
        FairValueGapCreatedEvent, OrderBlockCreatedEvent
    ]:
        bus.subscribe(event_type, lambda e: events_captured.append(e))

    # We will simulate a series of candles that forms a swing high, a swing low, a FVG, a BOS, and an Order Block.

    # Base price level
    p = 1.0000
    t = 1600000000
    
    def step_candle(h, l, c, o):
        nonlocal t
        t += 3600
        candle = make_candle(high=h, low=l, close=c, open_=o, timestamp=t)
        # We don't have a publisher for CandleClosedEvent in this test, 
        # so we'll call _on_candle directly or publish it.
        # Wait, MarketStructureService subscribes to CandleClosedEvent.
        from tradiba.market.events import CandleClosedEvent
        bus.publish(CandleClosedEvent(candle=candle))

    # Form a Swing High (requires 2 left, 1 mid, 2 right)
    # c1, c2, c3(high), c4, c5
    step_candle(1.0010, 1.0000, 1.0005, 1.0000) # c1
    step_candle(1.0020, 1.0010, 1.0015, 1.0010) # c2
    step_candle(1.0050, 1.0020, 1.0025, 1.0020) # c3 (High)
    step_candle(1.0030, 1.0010, 1.0015, 1.0020) # c4
    step_candle(1.0020, 1.0000, 1.0005, 1.0015) # c5 -> Swing High detected!
    
    assert any(isinstance(e, SwingHighEvent) for e in events_captured)
    
    # Now form a Swing Low
    # c6, c7, c8(low), c9, c10
    step_candle(1.0025, 1.0005, 1.0010, 1.0005) # c6
    step_candle(1.0015, 0.9990, 0.9995, 1.0010) # c7
    step_candle(1.0005, 0.9950, 0.9980, 0.9990) # c8 (Low)
    step_candle(1.0010, 0.9960, 0.9990, 0.9980) # c9
    step_candle(1.0015, 0.9970, 0.9995, 0.9990) # c10 -> Swing Low detected!
    
    assert any(isinstance(e, SwingLowEvent) for e in events_captured)
    
    # We now have a defined Swing High (1.0050) and Swing Low (0.9950)
    # Let's break the Swing High to trigger a BOS and establish Bullish Trend
    
    # c11: strong bullish candle (creates an order block later when broken?)
    # c11, c12, c13 for FVG
    step_candle(1.0020, 0.9990, 1.0015, 0.9995) # c11
    step_candle(1.0060, 1.0010, 1.0055, 1.0015) # c12 (Breaks 1.0050) -> BOS!
    
    assert any(isinstance(e, TrendChangedEvent) for e in events_captured)
    # The first break of a swing establishes trend. It is neutral initially.
    
    # c13: forms a FVG (c11.high = 1.0020, c13.low = 1.0030)
    step_candle(1.0080, 1.0030, 1.0070, 1.0055) # c13 -> FVG Created!
    
    assert any(isinstance(e, FairValueGapCreatedEvent) for e in events_captured)
    
    # Let's create another Swing High and then break it to get a BOS Event & Order Block
    step_candle(1.0090, 1.0050, 1.0060, 1.0070) # c14
    step_candle(1.0120, 1.0060, 1.0110, 1.0060) # c15 (High)
    step_candle(1.0110, 1.0070, 1.0080, 1.0110) # c16
    step_candle(1.0100, 1.0060, 1.0070, 1.0080) # c17 -> Swing High detected
    
    # Now a down candle before the break
    step_candle(1.0080, 1.0050, 1.0060, 1.0070) # c18 (down candle)
    
    # Now a strong bullish candle breaking 1.0120
    step_candle(1.0150, 1.0050, 1.0130, 1.0060) # c19 -> BOS! and Order Block!
    
    bos_events = [e for e in events_captured if isinstance(e, BOSEvent)]
    assert len(bos_events) > 0
    
    ob_events = [e for e in events_captured if isinstance(e, OrderBlockCreatedEvent)]
    assert len(ob_events) > 0

    svc.stop()
