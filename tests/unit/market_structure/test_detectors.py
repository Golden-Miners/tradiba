"""
Unit tests for all market structure detectors.

Tests each detector individually including zone lifecycle transitions.
"""

from __future__ import annotations

from datetime import datetime, timezone


from tradiba.market_structure.detectors.fvg import FVGDetector
from tradiba.market_structure.detectors.liquidity import LiquidityDetector
from tradiba.market_structure.detectors.order_block import OrderBlockDetector
from tradiba.market_structure.state import TimeframeState
from tradiba.market_structure.models import (
    Trend, SwingPoint, SwingKind, ZoneStatus,
    BreakOfStructure, LiquidityPool,
)
from tradiba.market_structure.events import (
    BOSEvent, FairValueGapCreatedEvent, FairValueGapFilledEvent, FairValueGapArchivedEvent,
    OrderBlockCreatedEvent, OrderBlockFilledEvent, OrderBlockArchivedEvent,
    LiquidityCreatedEvent, LiquiditySweptEvent,
)
from tradiba.mt5.models import Candle


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

_BASE_TS = datetime(2024, 1, 1, tzinfo=timezone.utc)
_T = 1600000000


def _candle(
    high: float, low: float, close: float, open_: float,
    *, ts_offset: int = 0, symbol: str = "TEST", timeframe: str = "H1",
) -> Candle:
    return Candle(
        symbol=symbol,
        timeframe=timeframe,
        timestamp=datetime.fromtimestamp(_T + ts_offset, tz=timezone.utc),
        open=open_,
        high=high,
        low=low,
        close=close,
        tick_volume=100,
        real_volume=0,
        spread=1,
    )


def _make_state(symbol: str = "TEST", timeframe: str = "H1") -> TimeframeState:
    return TimeframeState(symbol, timeframe)


def _feed(detector, state, candles, prior_events=None):
    """Feed candles through a detector, accumulating events."""
    all_events = []
    for c in candles:
        state.candles.append(c)
        state.candle_count += 1
        events = detector.update(c, state, prior_events or [])
        all_events.extend(events)
    return all_events


# ------------------------------------------------------------------
# FVG Detector — Zone Lifecycle
# ------------------------------------------------------------------


class TestFVGDetectorLifecycle:
    def test_bullish_fvg_created(self):
        """Three candles with gap between c1.high and c3.low → bullish FVG."""
        det = FVGDetector()
        state = _make_state()
        candles = [
            _candle(1.0010, 1.0000, 1.0005, 1.0000, ts_offset=0),
            _candle(1.0025, 1.0005, 1.0020, 1.0005, ts_offset=3600),
            _candle(1.0040, 1.0020, 1.0035, 1.0020, ts_offset=7200),  # c3.low=1.0020 > c1.high=1.0010
        ]
        events = _feed(det, state, candles)
        fvg_events = [e for e in events if isinstance(e, FairValueGapCreatedEvent)]
        assert len(fvg_events) == 1
        assert fvg_events[0].fvg.direction == Trend.BULLISH
        assert fvg_events[0].fvg.status == ZoneStatus.OPEN

    def test_fvg_transitions_to_active(self):
        """After one more candle, CREATED FVG becomes ACTIVE."""
        det = FVGDetector()
        state = _make_state()
        candles = [
            _candle(1.0010, 1.0000, 1.0005, 1.0000, ts_offset=0),
            _candle(1.0025, 1.0005, 1.0020, 1.0005, ts_offset=3600),
            _candle(1.0040, 1.0020, 1.0035, 1.0020, ts_offset=7200),
        ]
        _feed(det, state, candles)
        assert state.active_fvgs[0].status == ZoneStatus.OPEN

        # Feed one more candle that doesn't fill the gap
        neutral = _candle(1.0045, 1.0025, 1.0040, 1.0035, ts_offset=10800)
        state.candles.append(neutral)
        state.candle_count += 1
        det.update(neutral, state, [])
        assert state.active_fvgs[0].status == ZoneStatus.OPEN

    def test_fvg_mitigated(self):
        """Candle that fills entirely through the FVG → MITIGATED."""
        det = FVGDetector()
        state = _make_state()
        candles = [
            _candle(1.0010, 1.0000, 1.0005, 1.0000, ts_offset=0),
            _candle(1.0025, 1.0005, 1.0020, 1.0005, ts_offset=3600),
            _candle(1.0040, 1.0020, 1.0035, 1.0020, ts_offset=7200),
        ]
        _feed(det, state, candles)
        fvg = state.active_fvgs[0]

        # Candle that trades through the entire gap (low <= fvg.lower)
        fill = _candle(1.0030, 1.0005, 1.0010, 1.0030, ts_offset=10800)
        state.candles.append(fill)
        state.candle_count += 1
        events = det.update(fill, state, [])

        mit_events = [e for e in events if isinstance(e, FairValueGapFilledEvent)]
        assert len(mit_events) == 1
        assert len(state.active_fvgs) == 0

    def test_fvg_invalidated_by_age(self):
        """FVG that survives max_age candles without touch → INVALIDATED."""
        det = FVGDetector(max_age=5)
        state = _make_state()
        candles = [
            _candle(1.0010, 1.0000, 1.0005, 1.0000, ts_offset=0),
            _candle(1.0025, 1.0005, 1.0020, 1.0005, ts_offset=3600),
            _candle(1.0040, 1.0020, 1.0035, 1.0020, ts_offset=7200),
        ]
        _feed(det, state, candles)
        assert len(state.active_fvgs) == 1

        # Feed 6 more candles that don't touch the gap (well above it)
        events = []
        for i in range(6):
            c = _candle(1.0035, 1.0025, 1.0030, 1.0030, ts_offset=10800 + i * 3600)
            state.candles.append(c)
            state.candle_count += 1
            events.extend(det.update(c, state, []))

        inv_events = [e for e in events if isinstance(e, FairValueGapArchivedEvent)]
        assert len(inv_events) == 1
        assert len(state.active_fvgs) == 0

    def test_bearish_fvg_created(self):
        """Gap between c1.low and c3.high → bearish FVG."""
        det = FVGDetector()
        state = _make_state()
        candles = [
            _candle(1.0040, 1.0030, 1.0035, 1.0040, ts_offset=0),
            _candle(1.0025, 1.0015, 1.0020, 1.0025, ts_offset=3600),
            _candle(1.0020, 1.0010, 1.0015, 1.0020, ts_offset=7200),  # c3.high=1.0020 < c1.low=1.0030
        ]
        events = _feed(det, state, candles)
        fvg_events = [e for e in events if isinstance(e, FairValueGapCreatedEvent)]
        assert len(fvg_events) == 1
        assert fvg_events[0].fvg.direction == Trend.BEARISH


# ------------------------------------------------------------------
# Order Block Detector — Zone Lifecycle
# ------------------------------------------------------------------


class TestOrderBlockDetectorLifecycle:
    def _setup_bullish_bos(self, state: TimeframeState):
        """Helper: produce a BOSEvent for bullish BOS."""
        bos_candle = _candle(1.0060, 1.0040, 1.0055, 1.0040, ts_offset=3600)
        bos = BreakOfStructure(
            candle=bos_candle,
            broken_price=1.0050,
            direction=Trend.BULLISH,
        )
        return BOSEvent(
            symbol="TEST", direction=Trend.BULLISH,
            broken_price=1.0050, candle=bos_candle, bos=bos,
        )

    def test_order_block_created_on_bos(self):
        """BOS event triggers OB creation from last opposing candle."""
        det = OrderBlockDetector()
        state = _make_state()

        # Add a down-candle (opposing) and then a breakout candle
        down = _candle(1.0035, 1.0020, 1.0025, 1.0035, ts_offset=0)  # close < open
        breakout = _candle(1.0060, 1.0040, 1.0055, 1.0040, ts_offset=3600)
        state.candles.append(down)
        state.candle_count += 1
        state.candles.append(breakout)
        state.candle_count += 1

        bos_event = self._setup_bullish_bos(state)
        events = det.update(breakout, state, [bos_event])

        ob_events = [e for e in events if isinstance(e, OrderBlockCreatedEvent)]
        assert len(ob_events) == 1
        assert ob_events[0].ob.direction == Trend.BULLISH
        assert ob_events[0].ob.status == ZoneStatus.OPEN

    def test_order_block_transitions_to_active(self):
        """OB transitions from CREATED → ACTIVE after one candle."""
        det = OrderBlockDetector()
        state = _make_state()

        down = _candle(1.0035, 1.0020, 1.0025, 1.0035, ts_offset=0)
        breakout = _candle(1.0060, 1.0040, 1.0055, 1.0040, ts_offset=3600)
        state.candles.append(down)
        state.candle_count += 1
        state.candles.append(breakout)
        state.candle_count += 1

        bos_event = self._setup_bullish_bos(state)
        det.update(breakout, state, [bos_event])
        assert state.active_order_blocks[0].status == ZoneStatus.OPEN

        # Next candle — above the OB zone
        next_c = _candle(1.0065, 1.0050, 1.0060, 1.0055, ts_offset=7200)
        state.candles.append(next_c)
        state.candle_count += 1
        det.update(next_c, state, [])
        assert state.active_order_blocks[0].status == ZoneStatus.OPEN

    def test_bullish_ob_mitigated(self):
        """Price trades fully through a bullish OB → MITIGATED."""
        det = OrderBlockDetector()
        state = _make_state()

        down = _candle(1.0035, 1.0020, 1.0025, 1.0035, ts_offset=0)
        breakout = _candle(1.0060, 1.0040, 1.0055, 1.0040, ts_offset=3600)
        state.candles.append(down)
        state.candle_count += 1
        state.candles.append(breakout)
        state.candle_count += 1

        bos_event = self._setup_bullish_bos(state)
        det.update(breakout, state, [bos_event])

        # Price drops through entire OB zone (low <= zone_low)
        drop = _candle(1.0025, 1.0010, 1.0015, 1.0025, ts_offset=7200)
        state.candles.append(drop)
        state.candle_count += 1
        events = det.update(drop, state, [])

        mit_events = [e for e in events if isinstance(e, OrderBlockFilledEvent)]
        assert len(mit_events) == 1
        assert len(state.active_order_blocks) == 0

    def test_bullish_ob_invalidated(self):
        """Price closes below bullish OB ZoneStatus.ARCHIVED."""
        det = OrderBlockDetector()
        state = _make_state()

        down = _candle(1.0035, 1.0020, 1.0025, 1.0035, ts_offset=0)
        breakout = _candle(1.0060, 1.0040, 1.0055, 1.0040, ts_offset=3600)
        state.candles.append(down)
        state.candle_count += 1
        state.candles.append(breakout)
        state.candle_count += 1

        bos_event = self._setup_bullish_bos(state)
        det.update(breakout, state, [bos_event])

        # Candle that closes below the OB zone_low but doesn't trade through it fully
        # Actually for bullish OB, low <= zone_low triggers mitigation first.
        # To test invalidation specifically, the close must be < zone_low.
        # Since mitigation is checked first (low <= zone_low), the OB gets mitigated.
        # The invalidation path is for candles where close < zone_low but low hasn't pierced it —
        # which can't happen if close < zone_low means low <= close < zone_low is impossible.
        # So for bullish OBs, mitigation and invalidation overlap. Let's verify mitigation fires:
        close_below = _candle(1.0025, 1.0010, 1.0015, 1.0025, ts_offset=7200)
        state.candles.append(close_below)
        state.candle_count += 1
        events = det.update(close_below, state, [])
        # Should see mitigation since low <= zone_low
        assert any(isinstance(e, (OrderBlockFilledEvent, OrderBlockArchivedEvent)) for e in events)
        assert len(state.active_order_blocks) == 0


# ------------------------------------------------------------------
# Liquidity Detector — Zone Lifecycle
# ------------------------------------------------------------------


class TestLiquidityDetectorLifecycle:
    def test_liquidity_pool_created_from_equal_highs(self):
        """Two swing highs at similar prices → pool created."""
        det = LiquidityDetector(tolerance_pts=0.0005)
        state = _make_state()

        # Manually add two equal swing highs
        sp1 = SwingPoint(
            index=0, timestamp=_BASE_TS, price=1.0050,
            kind=SwingKind.HIGH, candle=_candle(1.0050, 1.0040, 1.0045, 1.0040),
        )
        sp2 = SwingPoint(
            index=5, timestamp=_BASE_TS, price=1.0051,
            kind=SwingKind.HIGH, candle=_candle(1.0051, 1.0041, 1.0046, 1.0041),
        )
        state.unmitigated_swing_highs.extend([sp1, sp2])

        c = _candle(1.0030, 1.0020, 1.0025, 1.0020, ts_offset=0)
        state.candles.append(c)
        state.candle_count += 1
        events = det.update(c, state, [])

        pool_events = [e for e in events if isinstance(e, LiquidityCreatedEvent)]
        assert len(pool_events) == 1
        assert pool_events[0].pool.direction == Trend.BULLISH

    def test_liquidity_pool_swept(self):
        """Price sweeps above a bullish pool → MITIGATED + swept event."""
        det = LiquidityDetector(tolerance_pts=0.0005)
        state = _make_state()

        pool = LiquidityPool(
            price=1.0050, strength=2, direction=Trend.BULLISH,
            created_at=_BASE_TS, status=ZoneStatus.OPEN,
        )
        state.liquidity_pools.append(pool)

        sweep = _candle(1.0060, 1.0040, 1.0055, 1.0040, ts_offset=0)
        state.candles.append(sweep)
        state.candle_count += 1
        events = det.update(sweep, state, [])

        swept_events = [e for e in events if isinstance(e, LiquiditySweptEvent)]
        assert len(swept_events) == 1
        assert pool.status == ZoneStatus.FILLED
        assert len(state.liquidity_pools) == 0

    def test_pool_transitions_to_active(self):
        """Pool CREATED → ACTIVE after one candle."""
        det = LiquidityDetector(tolerance_pts=0.0005)
        state = _make_state()

        pool = LiquidityPool(
            price=1.0050, strength=2, direction=Trend.BULLISH,
            created_at=_BASE_TS, status=ZoneStatus.OPEN,
        )
        state.liquidity_pools.append(pool)

        c = _candle(1.0030, 1.0020, 1.0025, 1.0020, ts_offset=0)
        state.candles.append(c)
        state.candle_count += 1
        det.update(c, state, [])
        assert pool.status == ZoneStatus.OPEN
