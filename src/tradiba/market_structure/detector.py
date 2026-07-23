"""
Market structure detection algorithms.

All functions are pure — they read state but never mutate it or
publish events.  This makes them trivially unit-testable.
"""

from __future__ import annotations

from collections import deque

from tradiba.mt5.models import Candle

from .models import (
    BreakOfStructure,
    ChangeOfCharacter,
    SwingHigh,
    SwingLow,
    Trend,
)
from .state import SWING_WINDOW, MarketStructureState


# ------------------------------------------------------------------
# Swing detection
# ------------------------------------------------------------------

def detect_swing_high(candles: deque[Candle]) -> SwingHigh | None:
    """
    Check whether the middle candle of a 5-candle window is a swing high.

    Returns a :class:`SwingHigh` if confirmed, otherwise ``None``.
    Strict inequality — a plateau does **not** count as a swing.
    """
    if len(candles) < SWING_WINDOW:
        return None

    c0, c1, c2, c3, c4 = (
        candles[-5],
        candles[-4],
        candles[-3],
        candles[-2],
        candles[-1],
    )

    if (
        c2.high > c0.high
        and c2.high > c1.high
        and c2.high > c3.high
        and c2.high > c4.high
    ):
        return SwingHigh(candle=c2, price=c2.high)

    return None


def detect_swing_low(candles: deque[Candle]) -> SwingLow | None:
    """
    Check whether the middle candle of a 5-candle window is a swing low.

    Returns a :class:`SwingLow` if confirmed, otherwise ``None``.
    Strict inequality — a plateau does **not** count as a swing.
    """
    if len(candles) < SWING_WINDOW:
        return None

    c0, c1, c2, c3, c4 = (
        candles[-5],
        candles[-4],
        candles[-3],
        candles[-2],
        candles[-1],
    )

    if (
        c2.low < c0.low
        and c2.low < c1.low
        and c2.low < c3.low
        and c2.low < c4.low
    ):
        return SwingLow(candle=c2, price=c2.low)

    return None


# ------------------------------------------------------------------
# Break of structure / change of character
# ------------------------------------------------------------------

def detect_structure_break(
    candle: Candle,
    state: MarketStructureState,
) -> BreakOfStructure | ChangeOfCharacter | None:
    """
    Check whether *candle* breaks a tracked swing level.

    Returns one of:

    * :class:`BreakOfStructure` — break in the direction of the trend.
    * :class:`ChangeOfCharacter` — break against the trend (reversal).
    * ``None`` — no break detected.

    Does **not** fire for a :attr:`Trend.NEUTRAL` state; the service
    handles initial trend establishment separately.
    """
    if state.trend == Trend.NEUTRAL:
        return None

    # -- upward break (close above last swing high) --------------------
    if (
        state.last_swing_high is not None
        and candle.close > state.last_swing_high.price
    ):
        if state.trend == Trend.BULLISH:
            return BreakOfStructure(
                candle=candle,
                broken_level=state.last_swing_high.price,
                direction=Trend.BULLISH,
            )
        # trend is BEARISH → reversal
        return ChangeOfCharacter(
            candle=candle,
            broken_level=state.last_swing_high.price,
            direction=Trend.BULLISH,
        )

    # -- downward break (close below last swing low) -------------------
    if (
        state.last_swing_low is not None
        and candle.close < state.last_swing_low.price
    ):
        if state.trend == Trend.BEARISH:
            return BreakOfStructure(
                candle=candle,
                broken_level=state.last_swing_low.price,
                direction=Trend.BEARISH,
            )
        # trend is BULLISH → reversal
        return ChangeOfCharacter(
            candle=candle,
            broken_level=state.last_swing_low.price,
            direction=Trend.BEARISH,
        )

    return None
