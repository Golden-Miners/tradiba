from datetime import datetime

from tradiba.ports.clock import Clock


class ReplayClock(Clock):

    def __init__(self):
        self._time = datetime.min

    def set(
        self,
        value: datetime,
    ):
        self._time = value

    def now(self):
        return self._time
