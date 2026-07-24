from typing import List, Dict, Optional, Tuple
from tradiba.events import Event
from tradiba.mt5.models import Candle
from tradiba.market_structure.state import MarketStructureState
from tradiba.market_structure.detectors import (
    SwingDetector,
    FVGDetector,
    LiquidityDetector,
    TrendDetector,
    OrderBlockDetector,
)

# Default swing detection params: (left_bars, right_bars)
_DEFAULT_SWING_PARAMS: Tuple[int, int] = (2, 2)


class MarketStructureEngine:
    """
    Pure domain state machine that processes candles and updates market structure.

    Orchestrates the sequence of market structure detectors in a fixed order:
        1. SwingDetector   — identify swing highs / lows
        2. TrendDetector   — detect BOS / CHOCH, update trend
        3. LiquidityDetector — cluster equal highs/lows, sweep detection
        4. FVGDetector     — Fair Value Gap creation and mitigation
        5. OrderBlockDetector — OB creation from BOS events, mitigation

    No detector should maintain isolated state; all read/write the shared
    ``TimeframeState`` object.
    """

    def __init__(
        self,
        swing_params: Optional[Dict[str, Tuple[int, int]]] = None,
        fvg_max_age: int = 50,
        liquidity_tolerance: float = 2.0,
    ) -> None:
        self.state: Dict[str, MarketStructureState] = {}

        # Per-timeframe swing params (left_bars, right_bars)
        self._swing_params = swing_params or {}
        self._fvg_max_age = fvg_max_age
        self._liquidity_tolerance = liquidity_tolerance

        # Default detectors — swing detector is created per-timeframe
        self._trend_detector = TrendDetector()
        self._liquidity_detector = LiquidityDetector(tolerance_pts=liquidity_tolerance)
        self._fvg_detector = FVGDetector(max_age=fvg_max_age)
        self._order_block_detector = OrderBlockDetector()

        # Cache of SwingDetector per-timeframe
        self._swing_detectors: Dict[str, SwingDetector] = {}

    def _get_swing_detector(self, timeframe: str) -> SwingDetector:
        if timeframe not in self._swing_detectors:
            left, right = self._swing_params.get(timeframe, _DEFAULT_SWING_PARAMS)
            self._swing_detectors[timeframe] = SwingDetector(left_bars=left, right_bars=right)
        return self._swing_detectors[timeframe]

    def on_candle(self, candle: Candle) -> List[Event]:
        # Get or create symbol state
        if candle.symbol not in self.state:
            self.state[candle.symbol] = MarketStructureState(candle.symbol)

        symbol_state = self.state[candle.symbol]

        # Get timeframe state
        tf_state = symbol_state.get_timeframe_state(candle.timeframe)

        # Update TimeframeState
        tf_state.candles.append(candle)
        tf_state.candle_count += 1

        current_events: List[Event] = []

        # Run candle through the sequence of detectors (order matters)
        swing_detector = self._get_swing_detector(candle.timeframe)
        detectors = [
            swing_detector,
            self._trend_detector,
            self._liquidity_detector,
            self._fvg_detector,
            self._order_block_detector,
        ]
        for detector in detectors:
            new_events = detector.update(candle, tf_state, current_events)
            current_events.extend(new_events)

        return current_events
