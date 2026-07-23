from datetime import datetime, timezone

from tradiba.ports.clock import Clock


class LiveClock(Clock):

    def now(self) -> datetime:
        return datetime.now(timezone.utc)
