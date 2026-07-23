"""
Deterministic tests for swing detection.

All tests use hand-crafted candles — no MT5 dependency.
"""

from __future__ import annotations

from collections import deque
from datetime import datetime, timezone

from tradiba.market_structure.detector import detect_swing_high, detect_swing_low
from tradiba.mt5.models import Candle


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

_BASE_TS = datetime(2024, 1, 1, tzinfo=timezone.utc)


def _candle(
    high: float,
    low: float,
    *,
    open_: float | None = None,
    close: float | None = None,
    minute: int = 0,
) -> Candle:
    """Build a minimal Candle for testing."""
    return Candle(
        symbol="TEST",
        timeframe="M1",
        timestamp=_BASE_TS.replace(minute=minute),
        open=open_ if open_ is not None else high,
        high=high,
        low=low,
        close=close if close is not None else low,
        tick_volume=1,
        spread=0,
        real_volume=0,
    )


def _make_deque(*candles: Candle) -> deque[Candle]:
    return deque(candles, maxlen=5)


# ------------------------------------------------------------------
# Swing high tests
# ------------------------------------------------------------------


class TestSwingHighDetection:
    def test_confirmed_swing_high(self):
        """C2 is the highest high → swing high detected."""
        candles = _make_deque(
            _candle(1.10, 1.08, minute=0),
            _candle(1.11, 1.09, minute=1),
            _candle(1.15, 1.10, minute=2),  # swing high
            _candle(1.12, 1.09, minute=3),
            _candle(1.11, 1.08, minute=4),
        )
        result = detect_swing_high(candles)
        assert result is not None
        assert result.price == 1.15
        assert result.candle.timestamp.minute == 2

    def test_no_swing_when_middle_is_not_highest(self):
        """C2 is NOT the highest → no swing."""
        candles = _make_deque(
            _candle(1.10, 1.08, minute=0),
            _candle(1.16, 1.09, minute=1),  # higher than C2
            _candle(1.15, 1.10, minute=2),
            _candle(1.12, 1.09, minute=3),
            _candle(1.11, 1.08, minute=4),
        )
        assert detect_swing_high(candles) is None

    def test_plateau_is_not_swing_high(self):
        """Equal highs at C1 and C2 → strict inequality fails → no swing."""
        candles = _make_deque(
            _candle(1.10, 1.08, minute=0),
            _candle(1.15, 1.09, minute=1),  # same as C2
            _candle(1.15, 1.10, minute=2),
            _candle(1.12, 1.09, minute=3),
            _candle(1.11, 1.08, minute=4),
        )
        assert detect_swing_high(candles) is None

    def test_not_enough_candles(self):
        """Fewer than 5 candles → no detection."""
        candles = deque(
            [_candle(1.10, 1.08, minute=i) for i in range(4)],
            maxlen=5,
        )
        assert detect_swing_high(candles) is None

    def test_right_neighbour_equals_candidate(self):
        """C3 equals C2 high → strict inequality fails."""
        candles = _make_deque(
            _candle(1.10, 1.08, minute=0),
            _candle(1.11, 1.09, minute=1),
            _candle(1.15, 1.10, minute=2),
            _candle(1.15, 1.09, minute=3),  # same as C2
            _candle(1.11, 1.08, minute=4),
        )
        assert detect_swing_high(candles) is None


# ------------------------------------------------------------------
# Swing low tests
# ------------------------------------------------------------------


class TestSwingLowDetection:
    def test_confirmed_swing_low(self):
        """C2 is the lowest low → swing low detected."""
        candles = _make_deque(
            _candle(1.12, 1.10, minute=0),
            _candle(1.11, 1.09, minute=1),
            _candle(1.10, 1.05, minute=2),  # swing low
            _candle(1.11, 1.08, minute=3),
            _candle(1.12, 1.09, minute=4),
        )
        result = detect_swing_low(candles)
        assert result is not None
        assert result.price == 1.05
        assert result.candle.timestamp.minute == 2

    def test_no_swing_when_middle_is_not_lowest(self):
        """C2 is NOT the lowest → no swing."""
        candles = _make_deque(
            _candle(1.12, 1.10, minute=0),
            _candle(1.11, 1.04, minute=1),  # lower than C2
            _candle(1.10, 1.05, minute=2),
            _candle(1.11, 1.08, minute=3),
            _candle(1.12, 1.09, minute=4),
        )
        assert detect_swing_low(candles) is None

    def test_plateau_is_not_swing_low(self):
        """Equal lows at C1 and C2 → strict inequality fails → no swing."""
        candles = _make_deque(
            _candle(1.12, 1.10, minute=0),
            _candle(1.11, 1.05, minute=1),  # same as C2
            _candle(1.10, 1.05, minute=2),
            _candle(1.11, 1.08, minute=3),
            _candle(1.12, 1.09, minute=4),
        )
        assert detect_swing_low(candles) is None

    def test_not_enough_candles(self):
        """Fewer than 5 candles → no detection."""
        candles = deque(
            [_candle(1.10, 1.08, minute=i) for i in range(3)],
            maxlen=5,
        )
        assert detect_swing_low(candles) is None


# ------------------------------------------------------------------
# Both swings at once
# ------------------------------------------------------------------


class TestDualSwingDetection:
    def test_swing_high_and_low_on_same_candle(self):
        """C2 is both the highest high and lowest low → both detected."""
        candles = _make_deque(
            _candle(1.10, 1.08, minute=0),
            _candle(1.11, 1.09, minute=1),
            _candle(1.15, 1.02, minute=2),  # widest range
            _candle(1.12, 1.06, minute=3),
            _candle(1.11, 1.07, minute=4),
        )
        assert detect_swing_high(candles) is not None
        assert detect_swing_low(candles) is not None
