"""
News risk filter for the strategy pipeline.

Rejects signals when high-impact news events are imminent.
"""

from __future__ import annotations

from datetime import timedelta

from tradiba.market.news import NewsProvider, Impact
from tradiba.ports.clock import get_clock
from tradiba.strategy.pipeline import StrategyFilter, PipelineContext


class NewsRiskFilter(StrategyFilter):
    """
    Pipeline filter that rejects signals when high-impact news
    is within ``minutes_before`` minutes.

    Uses a :class:`NewsProvider` abstraction; works with a
    ``NullNewsProvider`` by default (passes all signals through).
    """

    def __init__(
        self,
        news_provider: NewsProvider,
        minutes_before: int = 30,
        min_impact: Impact = Impact.HIGH,
    ) -> None:
        self._provider = news_provider
        self._minutes_before = minutes_before
        self._min_impact = min_impact

    def evaluate(self, ctx: PipelineContext) -> bool:
        now = get_clock().now()
        cutoff = now + timedelta(minutes=self._minutes_before)

        events = self._provider.upcoming_events(ctx.symbol)
        for ev in events:
            if ev.impact.value >= self._min_impact.value and ev.timestamp <= cutoff:
                return False  # Block signal — high-impact news imminent

        return True
