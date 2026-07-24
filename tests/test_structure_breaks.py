"""
Deterministic tests for BOS and CHOCH detection using TrendDetector.
"""

from __future__ import annotations

from datetime import datetime, timezone

from tradiba.market_structure.detectors.trend import TrendDetector
from tradiba.market_structure.state import TimeframeState
from tradiba.market_structure.models import (
    SwingPoint,
    SwingKind,
    Trend,
)
from tradiba.market_structure.events import BOSEvent, CHOCHEvent, TrendChangedEvent
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


def _swing_point(price: float, kind: SwingKind) -> SwingPoint:
    c = _candle(price, minute=0)
    return SwingPoint(
        index=0,
        timestamp=c.timestamp,
        price=price,
        kind=kind,
        candle=c,
    )


def _state(
    trend: Trend,
    swing_high: float | None = None,
    swing_low: float | None = None,
) -> TimeframeState:
    s = TimeframeState(symbol="TEST", timeframe="M1")
    s.trend = trend
    if swing_high is not None:
        s.last_swing_high = _swing_point(swing_high, SwingKind.HIGH)
    if swing_low is not None:
        s.last_swing_low = _swing_point(swing_low, SwingKind.LOW)
    return s


# ------------------------------------------------------------------
# BOS tests
# ------------------------------------------------------------------


class TestBreakOfStructure:
    def test_bullish_bos(self):
        """Uptrend + close above swing high → BOS bullish."""
        detector = TrendDetector()
        state = _state(Trend.BULLISH, swing_high=1.1500)
        candle = _candle(1.1510, minute=5)

        events = detector.update(candle, state, [])

        bos_events = [e for e in events if isinstance(e, BOSEvent)]
        assert len(bos_events) == 1
        assert bos_events[0].direction == Trend.BULLISH
        assert bos_events[0].broken_price == 1.1500
        # BOS is also in state history
        assert len(state.bos_history) == 1
        assert state.last_bos is not None

    def test_bearish_bos(self):
        """Downtrend + close below swing low → BOS bearish."""
        detector = TrendDetector()
        state = _state(Trend.BEARISH, swing_low=1.0800)
        candle = _candle(1.0790, minute=5)

        events = detector.update(candle, state, [])

        bos_events = [e for e in events if isinstance(e, BOSEvent)]
        assert len(bos_events) == 1
        assert bos_events[0].direction == Trend.BEARISH
        assert bos_events[0].broken_price == 1.0800

    def test_no_bos_when_close_equals_level(self):
        """Close exactly at the swing level → no break (strict inequality)."""
        detector = TrendDetector()
        state = _state(Trend.BULLISH, swing_high=1.1500)
        candle = _candle(1.1500, minute=5)

        events = detector.update(candle, state, [])
        assert len(events) == 0

    def test_no_bos_without_swing(self):
        """No swing tracked → no break possible."""
        detector = TrendDetector()
        state = _state(Trend.BULLISH)
        candle = _candle(1.2000, minute=5)

        events = detector.update(candle, state, [])
        assert len(events) == 0


# ------------------------------------------------------------------
# CHOCH tests
# ------------------------------------------------------------------


class TestChangeOfCharacter:
    def test_bearish_choch(self):
        """Uptrend + close below swing low → CHOCH bearish (reversal)."""
        detector = TrendDetector()
        state = _state(Trend.BULLISH, swing_low=1.0800)
        candle = _candle(1.0790, minute=5)

        events = detector.update(candle, state, [])

        choch_events = [e for e in events if isinstance(e, CHOCHEvent)]
        assert len(choch_events) == 1
        assert choch_events[0].choch.direction == Trend.BEARISH
        # CHOCH is also in state history
        assert len(state.choch_history) == 1
        assert state.last_choch is not None

    def test_bullish_choch(self):
        """Downtrend + close above swing high → CHOCH bullish (reversal)."""
        detector = TrendDetector()
        state = _state(Trend.BEARISH, swing_high=1.1500)
        candle = _candle(1.1510, minute=5)

        events = detector.update(candle, state, [])

        choch_events = [e for e in events if isinstance(e, CHOCHEvent)]
        assert len(choch_events) == 1
        assert choch_events[0].choch.direction == Trend.BULLISH

    def test_choch_reports_new_direction(self):
        """CHOCH direction is the NEW trend, not the old one."""
        detector = TrendDetector()
        state = _state(Trend.BULLISH, swing_low=1.0800)
        candle = _candle(1.0790, minute=5)

        events = detector.update(candle, state, [])

        choch_events = [e for e in events if isinstance(e, CHOCHEvent)]
        assert choch_events[0].choch.direction == Trend.BEARISH  # NEW direction

    def test_choch_changes_state_trend(self):
        """After CHOCH, state.trend should reflect the new direction."""
        detector = TrendDetector()
        state = _state(Trend.BULLISH, swing_low=1.0800)
        candle = _candle(1.0790, minute=5)

        detector.update(candle, state, [])
        assert state.trend == Trend.BEARISH

    def test_choch_emits_trend_changed_event(self):
        """CHOCH should also emit a TrendChangedEvent."""
        detector = TrendDetector()
        state = _state(Trend.BULLISH, swing_low=1.0800)
        candle = _candle(1.0790, minute=5)

        events = detector.update(candle, state, [])

        trend_events = [e for e in events if isinstance(e, TrendChangedEvent)]
        assert len(trend_events) == 1
        assert trend_events[0].old_trend == Trend.BULLISH
        assert trend_events[0].new_trend == Trend.BEARISH


# ------------------------------------------------------------------
# NEUTRAL trend tests
# ------------------------------------------------------------------


class TestNeutralTrend:
    def test_neutral_upward_establishes_bullish(self):
        """NEUTRAL + close above swing high → BULLISH trend established."""
        detector = TrendDetector()
        state = _state(Trend.NEUTRAL, swing_high=1.1500)
        candle = _candle(1.1600, minute=5)

        events = detector.update(candle, state, [])

        trend_events = [e for e in events if isinstance(e, TrendChangedEvent)]
        assert len(trend_events) == 1
        assert trend_events[0].new_trend == Trend.BULLISH
        assert state.trend == Trend.BULLISH

    def test_neutral_downward_establishes_bearish(self):
        """NEUTRAL + close below swing low → BEARISH trend established."""
        detector = TrendDetector()
        state = _state(Trend.NEUTRAL, swing_low=1.0800)
        candle = _candle(1.0700, minute=5)

        events = detector.update(candle, state, [])

        trend_events = [e for e in events if isinstance(e, TrendChangedEvent)]
        assert len(trend_events) == 1
        assert trend_events[0].new_trend == Trend.BEARISH
        assert state.trend == Trend.BEARISH

    def test_neutral_no_swings_returns_nothing(self):
        """NEUTRAL with no swings → nothing happens."""
        detector = TrendDetector()
        state = _state(Trend.NEUTRAL)
        candle = _candle(1.1000, minute=5)

        events = detector.update(candle, state, [])
        assert len(events) == 0
