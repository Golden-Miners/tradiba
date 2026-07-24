"""
Null implementation of NewsProvider — returns no events.

Used as the default/testing provider when no economic calendar is configured.
"""

from typing import List

from tradiba.market.news import NewsEvent, NewsProvider


class NullNewsProvider(NewsProvider):
    """Returns an empty list — all signals pass through."""

    def upcoming_events(self, symbol: str) -> List[NewsEvent]:
        return []
