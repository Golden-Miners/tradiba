"""
Deterministic tests for BOS and CHOCH detection.
"""

from __future__ import annotations

from datetime import datetime, timezone

from tradiba.market_structure.detector import detect_structure_break
from tradiba.market_structure.models import (
    BreakOfStructure,
    ChangeOfCharacter,
    SwingHigh,
    SwingLow,
    Trend,
)
from tradiba.market_structure.state import MarketStructureState
from tradiba.mt5.models import Candle


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

_BASE_TS = datetime(2024, 1, 1, tzinfo=timezone.utc)


def _candle(
    close: float,
    *,
    high: float | None = None,
    low: float | None = None,
    minute: int = 0,
) -> Candle:
    """Build a Candle focused on the close price for break tests."""
    h = high if high is not None else close + 0.001
    lo = low if low is not None else close - 0.001
    return Candle(
        symbol="TEST",
        timeframe="M1",
        timestamp=_BASE_TS.replace(minute=minute),
        open=close,
        high=h,
        low=lo,
        close=close,
        tick_volume=1,
        spread=0,
        real_volume=0,
    )


def _swing_high(price: float) -> SwingHigh:
    return SwingHigh(candle=_candle(price, minute=0), price=price)


def _swing_low(price: float) -> SwingLow:
    return SwingLow(candle=_candle(price, minute=0), price=price)


def _state(
    trend: Trend,
    swing_high: float | None = None,
    swing_low: float | None = None,
) -> MarketStructureState:
    s = MarketStructureState(symbol="TEST", timeframe="M1")
    s.trend = trend
    if swing_high is not None:
        s.last_swing_high = _swing_high(swing_high)
    if swing_low is not None:
        s.last_swing_low = _swing_low(swing_low)
    return s


# ------------------------------------------------------------------
# BOS tests
# ------------------------------------------------------------------


class TestBreakOfStructure:
    def test_bullish_bos(self):
        """Uptrend + close above swing high → BOS bullish."""
        state = _state(Trend.BULLISH, swing_high=1.1500)
        candle = _candle(1.1510, minute=5)  # closes above 1.1500

        result = detect_structure_break(candle, state)

        assert isinstance(result, BreakOfStructure)
        assert result.direction == Trend.BULLISH
        assert result.broken_level == 1.1500

    def test_bearish_bos(self):
        """Downtrend + close below swing low → BOS bearish."""
        state = _state(Trend.BEARISH, swing_low=1.0800)
        candle = _candle(1.0790, minute=5)  # closes below 1.0800

        result = detect_structure_break(candle, state)

        assert isinstance(result, BreakOfStructure)
        assert result.direction == Trend.BEARISH
        assert result.broken_level == 1.0800

    def test_no_bos_when_close_equals_level(self):
        """Close exactly at the swing level → no break (strict inequality)."""
        state = _state(Trend.BULLISH, swing_high=1.1500)
        candle = _candle(1.1500, minute=5)

        assert detect_structure_break(candle, state) is None

    def test_no_bos_without_swing(self):
        """No swing tracked → no break possible."""
        state = _state(Trend.BULLISH)  # no swing_high
        candle = _candle(1.2000, minute=5)

        assert detect_structure_break(candle, state) is None


# ------------------------------------------------------------------
# CHOCH tests
# ------------------------------------------------------------------


class TestChangeOfCharacter:
    def test_bearish_choch(self):
        """Uptrend + close below swing low → CHOCH bearish (reversal)."""
        state = _state(Trend.BULLISH, swing_low=1.0800)
        candle = _candle(1.0790, minute=5)

        result = detect_structure_break(candle, state)

        assert isinstance(result, ChangeOfCharacter)
        assert result.direction == Trend.BEARISH
        assert result.broken_level == 1.0800

    def test_bullish_choch(self):
        """Downtrend + close above swing high → CHOCH bullish (reversal)."""
        state = _state(Trend.BEARISH, swing_high=1.1500)
        candle = _candle(1.1510, minute=5)

        result = detect_structure_break(candle, state)

        assert isinstance(result, ChangeOfCharacter)
        assert result.direction == Trend.BULLISH
        assert result.broken_level == 1.1500

    def test_choch_reports_new_direction(self):
        """CHOCH direction is the NEW trend, not the old one."""
        state = _state(Trend.BULLISH, swing_low=1.0800)
        candle = _candle(1.0790, minute=5)

        result = detect_structure_break(candle, state)

        assert isinstance(result, ChangeOfCharacter)
        assert result.direction == Trend.BEARISH  # NEW direction


# ------------------------------------------------------------------
# NEUTRAL trend tests
# ------------------------------------------------------------------


class TestNeutralTrend:
    def test_neutral_returns_none(self):
        """NEUTRAL trend → no BOS or CHOCH (handled separately by service)."""
        state = _state(Trend.NEUTRAL, swing_high=1.1500, swing_low=1.0800)
        candle = _candle(1.1600, minute=5)  # breaks above swing high

        assert detect_structure_break(candle, state) is None

    def test_neutral_downward_break_returns_none(self):
        """NEUTRAL trend + downward break → still None."""
        state = _state(Trend.NEUTRAL, swing_high=1.1500, swing_low=1.0800)
        candle = _candle(1.0700, minute=5)  # breaks below swing low

        assert detect_structure_break(candle, state) is None
