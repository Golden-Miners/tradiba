"""
Deterministic tests for swing detection using SwingDetector.

All tests use hand-crafted candles — no MT5 dependency.
"""

from __future__ import annotations

from datetime import datetime, timezone

from tradiba.market_structure.detectors.swing import SwingDetector
from tradiba.market_structure.state import TimeframeState
from tradiba.market_structure.events import SwingHighEvent, SwingLowEvent
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


def _feed_candles(detector: SwingDetector, state: TimeframeState, candles: list[Candle]):
    """Feed a sequence of candles through the detector, returning all events."""
    all_events = []
    for c in candles:
        state.candles.append(c)
        state.candle_count += 1
        events = detector.update(c, state, [])
        all_events.extend(events)
    return all_events


# ------------------------------------------------------------------
# Swing high tests
# ------------------------------------------------------------------


class TestSwingHighDetection:
    def test_confirmed_swing_high(self):
        """C2 is the highest high → swing high detected."""
        detector = SwingDetector(left_bars=2, right_bars=2)
        state = TimeframeState("TEST", "M1")
        candles = [
            _candle(1.10, 1.08, minute=0),
            _candle(1.11, 1.09, minute=1),
            _candle(1.15, 1.10, minute=2),  # swing high
            _candle(1.12, 1.09, minute=3),
            _candle(1.11, 1.08, minute=4),
        ]
        events = _feed_candles(detector, state, candles)
        high_events = [e for e in events if isinstance(e, SwingHighEvent)]
        assert len(high_events) == 1
        assert high_events[0].swing.price == 1.15

    def test_no_swing_when_middle_is_not_highest(self):
        """C2 is NOT the highest → no swing."""
        detector = SwingDetector(left_bars=2, right_bars=2)
        state = TimeframeState("TEST", "M1")
        candles = [
            _candle(1.10, 1.08, minute=0),
            _candle(1.16, 1.09, minute=1),  # higher than C2
            _candle(1.15, 1.10, minute=2),
            _candle(1.12, 1.09, minute=3),
            _candle(1.11, 1.08, minute=4),
        ]
        events = _feed_candles(detector, state, candles)
        high_events = [e for e in events if isinstance(e, SwingHighEvent)]
        assert len(high_events) == 0

    def test_plateau_is_not_swing_high(self):
        """Equal highs at C1 and C2 → strict inequality fails → no swing."""
        detector = SwingDetector(left_bars=2, right_bars=2)
        state = TimeframeState("TEST", "M1")
        candles = [
            _candle(1.10, 1.08, minute=0),
            _candle(1.15, 1.09, minute=1),  # same as C2
            _candle(1.15, 1.10, minute=2),
            _candle(1.12, 1.09, minute=3),
            _candle(1.11, 1.08, minute=4),
        ]
        events = _feed_candles(detector, state, candles)
        high_events = [e for e in events if isinstance(e, SwingHighEvent)]
        assert len(high_events) == 0

    def test_not_enough_candles(self):
        """Fewer than 5 candles → no detection."""
        detector = SwingDetector(left_bars=2, right_bars=2)
        state = TimeframeState("TEST", "M1")
        candles = [_candle(1.10, 1.08, minute=i) for i in range(4)]
        events = _feed_candles(detector, state, candles)
        assert len(events) == 0

    def test_right_neighbour_equals_candidate(self):
        """C3 equals C2 high → strict inequality fails."""
        detector = SwingDetector(left_bars=2, right_bars=2)
        state = TimeframeState("TEST", "M1")
        candles = [
            _candle(1.10, 1.08, minute=0),
            _candle(1.11, 1.09, minute=1),
            _candle(1.15, 1.10, minute=2),
            _candle(1.15, 1.09, minute=3),  # same as C2
            _candle(1.11, 1.08, minute=4),
        ]
        events = _feed_candles(detector, state, candles)
        high_events = [e for e in events if isinstance(e, SwingHighEvent)]
        assert len(high_events) == 0


# ------------------------------------------------------------------
# Swing low tests
# ------------------------------------------------------------------


class TestSwingLowDetection:
    def test_confirmed_swing_low(self):
        """C2 is the lowest low → swing low detected."""
        detector = SwingDetector(left_bars=2, right_bars=2)
        state = TimeframeState("TEST", "M1")
        candles = [
            _candle(1.12, 1.10, minute=0),
            _candle(1.11, 1.09, minute=1),
            _candle(1.10, 1.05, minute=2),  # swing low
            _candle(1.11, 1.08, minute=3),
            _candle(1.12, 1.09, minute=4),
        ]
        events = _feed_candles(detector, state, candles)
        low_events = [e for e in events if isinstance(e, SwingLowEvent)]
        assert len(low_events) == 1
        assert low_events[0].swing.price == 1.05

    def test_no_swing_when_middle_is_not_lowest(self):
        """C2 is NOT the lowest → no swing."""
        detector = SwingDetector(left_bars=2, right_bars=2)
        state = TimeframeState("TEST", "M1")
        candles = [
            _candle(1.12, 1.10, minute=0),
            _candle(1.11, 1.04, minute=1),  # lower than C2
            _candle(1.10, 1.05, minute=2),
            _candle(1.11, 1.08, minute=3),
            _candle(1.12, 1.09, minute=4),
        ]
        events = _feed_candles(detector, state, candles)
        low_events = [e for e in events if isinstance(e, SwingLowEvent)]
        assert len(low_events) == 0

    def test_plateau_is_not_swing_low(self):
        """Equal lows at C1 and C2 → strict inequality fails → no swing."""
        detector = SwingDetector(left_bars=2, right_bars=2)
        state = TimeframeState("TEST", "M1")
        candles = [
            _candle(1.12, 1.10, minute=0),
            _candle(1.11, 1.05, minute=1),  # same as C2
            _candle(1.10, 1.05, minute=2),
            _candle(1.11, 1.08, minute=3),
            _candle(1.12, 1.09, minute=4),
        ]
        events = _feed_candles(detector, state, candles)
        low_events = [e for e in events if isinstance(e, SwingLowEvent)]
        assert len(low_events) == 0

    def test_not_enough_candles(self):
        """Fewer than 5 candles → no detection."""
        detector = SwingDetector(left_bars=2, right_bars=2)
        state = TimeframeState("TEST", "M1")
        candles = [_candle(1.10, 1.08, minute=i) for i in range(3)]
        events = _feed_candles(detector, state, candles)
        assert len(events) == 0


# ------------------------------------------------------------------
# Both swings at once
# ------------------------------------------------------------------


class TestDualSwingDetection:
    def test_swing_high_and_low_on_same_candle(self):
        """C2 is both the highest high and lowest low → both detected."""
        detector = SwingDetector(left_bars=2, right_bars=2)
        state = TimeframeState("TEST", "M1")
        candles = [
            _candle(1.10, 1.08, minute=0),
            _candle(1.11, 1.09, minute=1),
            _candle(1.15, 1.02, minute=2),  # widest range
            _candle(1.12, 1.06, minute=3),
            _candle(1.11, 1.07, minute=4),
        ]
        events = _feed_candles(detector, state, candles)
        assert any(isinstance(e, SwingHighEvent) for e in events)
        assert any(isinstance(e, SwingLowEvent) for e in events)
