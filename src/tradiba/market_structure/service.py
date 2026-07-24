from tradiba.market.events import CandleClosedEvent

from .detector import SwingDetector


class MarketStructureService:

    def __init__(
        self,
        event_bus,
    ):
        self._event_bus = event_bus
        self._detector = SwingDetector()

    def on_candle_closed(
        self,
        event: CandleClosedEvent,
    ):

        swing = self._detector.update(event.candle)

        if swing is not None:
            self._event_bus.publish(swing)

    def start(self):
        pass

    def stop(self):
        pass
