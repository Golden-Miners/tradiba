from datetime import datetime, timezone
from tradiba.market.models import Candle, Timeframe
from tradiba.market_structure.models import SwingPoint, SwingType, LiquidityStatus
from tradiba.market_structure.state import MarketStructureState
from tradiba.market_structure.liquidity import LiquidityDetector
from tradiba.market_structure.events import LiquidityCreatedEvent, LiquiditySweptEvent

def candle(price: float, t: int = 1, h: float = None, low: float = None) -> Candle:
    if h is None:
        h = price
    if low is None:
        low = price
    return Candle(
        symbol="EURUSD",
        timeframe=Timeframe.M1,
        open_time=datetime(2025, 1, 1, 12, t, 0, tzinfo=timezone.utc),
        open=price,
        high=h,
        low=low,
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

def test_equal_highs():
    state = MarketStructureState()
    detector = LiquidityDetector(tolerance=0.00010, min_touches=2)
    
    events1 = detector.update_swing(swing(1.1050, SwingType.HIGH), state)
    assert len(events1) == 0 # Only 1 touch
    assert len(state.active_liquidity) == 1
    
    events2 = detector.update_swing(swing(1.10505, SwingType.HIGH), state)
    assert len(events2) == 1 # 2nd touch, emits created
    assert isinstance(events2[0], LiquidityCreatedEvent)
    assert events2[0].pool.touches == 2

def test_equal_lows():
    state = MarketStructureState()
    detector = LiquidityDetector(tolerance=0.00010, min_touches=2)
    
    events1 = detector.update_swing(swing(1.0920, SwingType.LOW), state)
    assert len(events1) == 0
    
    events2 = detector.update_swing(swing(1.09195, SwingType.LOW), state)
    assert len(events2) == 1
    assert isinstance(events2[0], LiquidityCreatedEvent)
    assert events2[0].pool.touches == 2

def test_no_match():
    state = MarketStructureState()
    detector = LiquidityDetector(tolerance=0.00010, min_touches=2)
    
    events1 = detector.update_swing(swing(1.1000, SwingType.HIGH), state)
    assert len(events1) == 0
    assert len(state.active_liquidity) == 1
    
    events2 = detector.update_swing(swing(1.1100, SwingType.HIGH), state)
    assert len(events2) == 0 # Out of tolerance, creates a new pool
    assert len(state.active_liquidity) == 2

def test_buy_side_sweep():
    state = MarketStructureState()
    detector = LiquidityDetector(tolerance=0.00010, min_touches=2)
    
    # Create EQH
    detector.update_swing(swing(1.1050, SwingType.HIGH), state)
    detector.update_swing(swing(1.1050, SwingType.HIGH), state)
    
    # Next candle sweeps
    c = candle(1.1040, h=1.1055, l=1.1030)
    sweep_events = detector.check_sweep(c, state)
    
    assert len(sweep_events) == 1
    assert isinstance(sweep_events[0], LiquiditySweptEvent)
    assert sweep_events[0].pool.status == LiquidityStatus.SWEPT

def test_sell_side_sweep():
    state = MarketStructureState()
    detector = LiquidityDetector(tolerance=0.00010, min_touches=2)
    
    # Create EQL
    detector.update_swing(swing(1.0900, SwingType.LOW), state)
    detector.update_swing(swing(1.0900, SwingType.LOW), state)
    
    # Next candle sweeps
    c = candle(1.0910, h=1.0920, l=1.0897)
    sweep_events = detector.check_sweep(c, state)
    
    assert len(sweep_events) == 1
    assert isinstance(sweep_events[0], LiquiditySweptEvent)
    assert sweep_events[0].pool.status == LiquidityStatus.SWEPT

def test_no_sweep_if_not_minimum_touches():
    state = MarketStructureState()
    detector = LiquidityDetector(tolerance=0.00010, min_touches=2)
    
    # Create single touch
    detector.update_swing(swing(1.0900, SwingType.LOW), state)
    
    # Next candle sweeps the level, but since touches=1, it's not a valid pool
    c = candle(1.0910, h=1.0920, l=1.0897)
    sweep_events = detector.check_sweep(c, state)
    
    assert len(sweep_events) == 0
