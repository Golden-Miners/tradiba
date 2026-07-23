"""
Market structure analysis service.

Subscribes to :class:`CandleClosedEvent` and publishes swing,
BOS, and CHOCH events as price-action patterns are detected.
"""

from __future__ import annotations

from tradiba.core.service import Service
from tradiba.events import EventBus
from tradiba.logging import get_logger
from tradiba.market.events import CandleClosedEvent
from tradiba.mt5.models import Candle

from .detector import detect_structure_break, detect_swing_high, detect_swing_low
from .events import (
    BreakOfStructureEvent,
    ChangeOfCharacterEvent,
    SwingHighDetectedEvent,
    SwingLowDetectedEvent,
)
from .models import BreakOfStructure, ChangeOfCharacter, Trend
from .state import MarketStructureState

logger = get_logger(__name__)


class MarketStructureService(Service):
    """
    Analyses candle data and emits market structure events.

    Maintains a :class:`MarketStructureState` per ``(symbol, timeframe)``
    and runs swing + structure-break detection on every new candle.
    """

    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._states: dict[tuple[str, str], MarketStructureState] = {}

    # ------------------------------------------------------------------
    # Service lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        self._event_bus.subscribe(CandleClosedEvent, self._on_candle)
        logger.info("Market structure service started.")

    def stop(self) -> None:
        self._event_bus.unsubscribe(CandleClosedEvent, self._on_candle)
        self._states.clear()
        logger.info("Market structure service stopped.")

    # ------------------------------------------------------------------
    # Event handler
    # ------------------------------------------------------------------

    def _on_candle(self, event: CandleClosedEvent) -> None:
        candle = event.candle
        state = self._get_or_create_state(candle)

        state.candles.append(candle)

        # --- Swing detection ------------------------------------------
        swing_high = detect_swing_high(state.candles)
        if swing_high is not None:
            state.last_swing_high = swing_high
            self._event_bus.publish(SwingHighDetectedEvent(swing=swing_high))
            logger.debug(
                "Swing high: %s %s @ %.5f",
                candle.symbol,
                candle.timeframe,
                swing_high.price,
            )

        swing_low = detect_swing_low(state.candles)
        if swing_low is not None:
            state.last_swing_low = swing_low
            self._event_bus.publish(SwingLowDetectedEvent(swing=swing_low))
            logger.debug(
                "Swing low: %s %s @ %.5f",
                candle.symbol,
                candle.timeframe,
                swing_low.price,
            )

        # --- Initial trend establishment (NEUTRAL) --------------------
        if state.trend == Trend.NEUTRAL:
            self._try_set_initial_trend(candle, state)
            return

        # --- BOS / CHOCH detection ------------------------------------
        result = detect_structure_break(candle, state)

        if isinstance(result, BreakOfStructure):
            self._handle_bos(result, state)
        elif isinstance(result, ChangeOfCharacter):
            self._handle_choch(result, state)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_or_create_state(self, candle: Candle) -> MarketStructureState:
        key = (candle.symbol, candle.timeframe)
        if key not in self._states:
            self._states[key] = MarketStructureState(
                symbol=candle.symbol,
                timeframe=candle.timeframe,
            )
        return self._states[key]

    def _try_set_initial_trend(
        self,
        candle: Candle,
        state: MarketStructureState,
    ) -> None:
        """Set the initial trend direction without emitting an event."""
        if (
            state.last_swing_high is not None
            and candle.close > state.last_swing_high.price
        ):
            state.trend = Trend.BULLISH
            state.last_swing_high = None  # level consumed
            logger.info(
                "Initial trend BULLISH for %s %s",
                state.symbol,
                state.timeframe,
            )
        elif (
            state.last_swing_low is not None
            and candle.close < state.last_swing_low.price
        ):
            state.trend = Trend.BEARISH
            state.last_swing_low = None  # level consumed
            logger.info(
                "Initial trend BEARISH for %s %s",
                state.symbol,
                state.timeframe,
            )

    def _handle_bos(
        self,
        bos: BreakOfStructure,
        state: MarketStructureState,
    ) -> None:
        # Clear the broken level so it doesn't re-trigger.
        if bos.direction == Trend.BULLISH:
            state.last_swing_high = None
        else:
            state.last_swing_low = None

        self._event_bus.publish(BreakOfStructureEvent(bos=bos))
        logger.info(
            "BOS %s %s %s @ %.5f",
            bos.direction.value,
            state.symbol,
            state.timeframe,
            bos.broken_level,
        )

    def _handle_choch(
        self,
        choch: ChangeOfCharacter,
        state: MarketStructureState,
    ) -> None:
        # Flip the trend and clear the broken level.
        state.trend = choch.direction
        if choch.direction == Trend.BULLISH:
            state.last_swing_high = None
        else:
            state.last_swing_low = None

        self._event_bus.publish(ChangeOfCharacterEvent(choch=choch))
        logger.info(
            "CHOCH → %s %s %s @ %.5f",
            choch.direction.value,
            state.symbol,
            state.timeframe,
            choch.broken_level,
        )
