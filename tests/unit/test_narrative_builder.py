from datetime import datetime, timezone
from tradiba.market.models import Candle, Timeframe
from tradiba.market_structure.models import (
    Trend,
    OrderBlock,
    OrderBlockDirection,
    OrderBlockStatus,
    FairValueGap,
    FVGStatus,
    SwingPoint,
    SwingType,
)
from tradiba.market_structure.state import MarketStructureState
from tradiba.market_structure.narrative_builder import NarrativeBuilder
from tradiba.market_structure.narrative import MarketBias

def test_bullish_trend_produces_bullish_bias():
    state = MarketStructureState()
    state.trend = Trend.BULLISH
    builder = NarrativeBuilder()
    
    candle = Candle(
        symbol="EURUSD",
        timeframe=Timeframe.H1,
        open_time=datetime.now(timezone.utc),
        open=1.1000, high=1.1000, low=1.1000, close=1.1000, volume=100
    )
    
    narrative = builder.build(state, candle)
    
    # 25 points for Bullish Trend -> >= 20 -> BULLISH
    assert narrative.bias == MarketBias.BULLISH
    assert narrative.confidence == 25

def test_confidence_increases_with_confirmations():
    state = MarketStructureState()
    state.trend = Trend.BULLISH
    state.choch_detected = True
    
    # Add active Bullish OB
    ob = OrderBlock("id", "EURUSD", "H1", OrderBlockDirection.BULLISH, 1.10, 1.09, 1.11, datetime.now(), OrderBlockStatus.ACTIVE)
    state.active_order_blocks.append(ob)
    
    # Add active Bullish FVG
    state.active_fvgs = [
        FairValueGap("id", "EURUSD", "H1", Trend.BULLISH, 1.11, 1.10, datetime.now(), FVGStatus.ACTIVE)
    ]
    
    # Discount pricing
    state.last_swing_high = SwingPoint("EURUSD", "H1", SwingType.HIGH, datetime.now(), 1.20, None)
    state.last_swing_low = SwingPoint("EURUSD", "H1", SwingType.LOW, datetime.now(), 1.00, None)
    
    candle = Candle("EURUSD", Timeframe.H1, datetime.now(timezone.utc), 1.05, 1.05, 1.05, 1.05, 100)
    
    builder = NarrativeBuilder()
    narrative = builder.build(state, candle)
    
    # Score: Trend(+25) + CHOCH(+15) + OB(+20) + FVG(+15) + Discount(+10) = 85
    assert narrative.confidence == 85
    assert narrative.bias == MarketBias.STRONG_BULLISH

def test_mitigated_order_blocks_excluded():
    state = MarketStructureState()
    ob1 = OrderBlock("1", "EURUSD", "H1", OrderBlockDirection.BULLISH, 1.10, 1.09, 1.11, datetime.now(), OrderBlockStatus.ACTIVE)
    ob2 = OrderBlock("2", "EURUSD", "H1", OrderBlockDirection.BULLISH, 1.10, 1.09, 1.11, datetime.now(), OrderBlockStatus.MITIGATED)
    state.active_order_blocks.extend([ob1, ob2])
    
    candle = Candle("EURUSD", Timeframe.H1, datetime.now(timezone.utc), 1.05, 1.05, 1.05, 1.05, 100)
    builder = NarrativeBuilder()
    narrative = builder.build(state, candle)
    
    assert len(narrative.order_blocks) == 1
    assert narrative.order_blocks[0].id == "1"

def test_filled_fvgs_excluded():
    state = MarketStructureState()
    fvg1 = FairValueGap("1", "EURUSD", "H1", Trend.BULLISH, 1.11, 1.10, datetime.now(), FVGStatus.ACTIVE)
    fvg2 = FairValueGap("2", "EURUSD", "H1", Trend.BULLISH, 1.11, 1.10, datetime.now(), FVGStatus.FILLED)
    state.active_fvgs = [fvg1, fvg2]
    
    candle = Candle("EURUSD", Timeframe.H1, datetime.now(timezone.utc), 1.05, 1.05, 1.05, 1.05, 100)
    builder = NarrativeBuilder()
    narrative = builder.build(state, candle)
    
    assert len(narrative.fvgs) == 1
    assert narrative.fvgs[0].id == "1"

def test_premium_discount_bounds():
    state = MarketStructureState()
    state.last_swing_high = SwingPoint("EURUSD", "H1", SwingType.HIGH, datetime.now(), 1.20, None)
    state.last_swing_low = SwingPoint("EURUSD", "H1", SwingType.LOW, datetime.now(), 1.00, None)
    
    builder = NarrativeBuilder()
    
    # Below low -> clamped to 0.0
    c_low = Candle("EURUSD", Timeframe.H1, datetime.now(timezone.utc), 0.90, 0.90, 0.90, 0.90, 100)
    n1 = builder.build(state, c_low)
    assert n1.premium_discount == 0.0
    
    # Above high -> clamped to 1.0
    c_high = Candle("EURUSD", Timeframe.H1, datetime.now(timezone.utc), 1.30, 1.30, 1.30, 1.30, 100)
    n2 = builder.build(state, c_high)
    assert n2.premium_discount == 1.0
    
    # Midpoint -> 0.5
    c_mid = Candle("EURUSD", Timeframe.H1, datetime.now(timezone.utc), 1.10, 1.10, 1.10, 1.10, 100)
    n3 = builder.build(state, c_mid)
    import pytest
    assert n3.premium_discount == pytest.approx(0.5)
