from tradiba.market.models import Candle
from tradiba.market_structure.models import Trend, LiquidityStatus, OrderBlockStatus, OrderBlockDirection, FVGStatus
from tradiba.market_structure.state import MarketStructureState
from tradiba.market_structure.narrative import MarketNarrative, MarketBias


class NarrativeBuilder:
    def build(self, state: MarketStructureState, candle: Candle) -> MarketNarrative:
        
        # 1. Filter active zones
        active_liquidity = tuple(
            lp for lp in state.active_liquidity 
            if lp.status == LiquidityStatus.ACTIVE
        )
        # Note: state.active_fvgs now exists
        active_fvgs = tuple(
            fvg for fvg in state.active_fvgs
            if fvg.status == FVGStatus.ACTIVE
        )
        active_obs = tuple(
            ob for ob in state.active_order_blocks
            if ob.status in (OrderBlockStatus.ACTIVE, OrderBlockStatus.TOUCHED)
        )

        # 2. Premium / Discount
        premium_discount = 0.5
        if state.last_swing_high and state.last_swing_low:
            h = state.last_swing_high.price
            l = state.last_swing_low.price
            if h > l:
                premium_discount = (candle.close - l) / (h - l)
                premium_discount = max(0.0, min(1.0, premium_discount))

        # 3. Confidence & Bias Calculation
        bullish_score = 0
        bearish_score = 0

        if state.trend == Trend.BULLISH:
            bullish_score += 25
        elif state.trend == Trend.BEARISH:
            bearish_score += 25

        if state.choch_detected:
            if state.trend == Trend.BULLISH:
                bullish_score += 15
            elif state.trend == Trend.BEARISH:
                bearish_score += 15

        if any(ob.direction == OrderBlockDirection.BULLISH for ob in active_obs):
            bullish_score += 20
        if any(ob.direction == OrderBlockDirection.BEARISH for ob in active_obs):
            bearish_score += 20

        if any(fvg.direction == Trend.BULLISH for fvg in active_fvgs):
            bullish_score += 15
        if any(fvg.direction == Trend.BEARISH for fvg in active_fvgs):
            bearish_score += 15

        if premium_discount < 0.5:
            bullish_score += 10
        elif premium_discount > 0.5:
            bearish_score += 10

        # Also consider swept liquidity (if we wanted to check the history, 
        # but since we only have active, we just use the current scores)

        net_score = bullish_score - bearish_score
        confidence = min(100, max(bullish_score, bearish_score))

        if net_score >= 50:
            bias = MarketBias.STRONG_BULLISH
        elif net_score >= 20:
            bias = MarketBias.BULLISH
        elif net_score <= -50:
            bias = MarketBias.STRONG_BEARISH
        elif net_score <= -20:
            bias = MarketBias.BEARISH
        else:
            bias = MarketBias.NEUTRAL

        return MarketNarrative(
            symbol=candle.symbol,
            timeframe=candle.timeframe.name if hasattr(candle.timeframe, "name") else str(candle.timeframe),
            current_price=candle.close,
            timestamp=candle.open_time,
            trend=state.trend,
            bias=bias,
            confidence=confidence,
            premium_discount=premium_discount,
            liquidity=active_liquidity,
            fvgs=active_fvgs,
            order_blocks=active_obs,
        )
