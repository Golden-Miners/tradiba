from typing import List, Dict, Optional, Tuple
from tradiba.events import DomainEvent
from tradiba.mt5.models import Candle
from tradiba.market_structure.state import MarketStructureState
from tradiba.market_structure.detectors import (
    SwingDetector,
    FVGDetector,
    LiquidityDetector,
    OrderBlockDetector,
)
from tradiba.market_structure.bos import BOSDetector
from tradiba.market_structure.choch import CHOCHDetector

# Default swing detection params: (left_bars, right_bars)
_DEFAULT_SWING_PARAMS: Tuple[int, int] = (2, 2)


class MarketStructureEngine:
    """
    Pure domain state machine that processes candles and updates market structure.

    Orchestrates the sequence of market structure detectors in a fixed order:
        1. SwingDetector   — identify swing highs / lows
        2. BOSDetector     — detect Break of Structure events
        3. CHOCHDetector   — detect Change of Character events
        4. LiquidityDetector — cluster equal highs/lows, sweep detection
        5. FVGDetector     — Fair Value Gap creation and mitigation
        6. OrderBlockDetector — OB creation from BOS events, mitigation

    No detector should maintain isolated state; all read/write the shared
    ``MarketStructureState`` object.
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
        self._bos_detector = BOSDetector()
        self._choch_detector = CHOCHDetector()
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

    def on_candle(self, candle: Candle) -> List[DomainEvent]:
        # Get or create symbol state
        state_key = f'{candle.symbol}_{candle.timeframe}'
        if state_key not in self.state:
            self.state[state_key] = MarketStructureState()

        tf_state = self.state[state_key]

        # Update MarketStructureState
        tf_state.candles.append(candle)
        tf_state.candle_count += 1

        current_events: List[DomainEvent] = []

        # Run candle through the sequence of detectors (order matters)
        swing_detector = self._get_swing_detector(candle.timeframe)
        detectors = [
            swing_detector,
            self._bos_detector,
            self._choch_detector,
            self._liquidity_detector,
            self._fvg_detector,
            self._order_block_detector,
        ]
        for detector in detectors:
            new_events = detector.update(candle, tf_state, current_events)
            current_events.extend(new_events)

        return current_events
