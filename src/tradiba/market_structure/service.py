from tradiba.market.events import CandleClosedEvent

from .detector import SwingDetector
from .bos import BOSDetector
from .events import SwingHighEvent


class MarketStructureService:

    def __init__(
        self,
        event_bus,
    ):
        self.bus = event_bus
        self.swing_detector = SwingDetector()
        self.bos = BOSDetector()

    def on_candle_closed(
        self,
        event: CandleClosedEvent,
    ):

        swing = self.swing_detector.update(event.candle)

        if swing:

            self.bus.publish(swing)

            if isinstance(swing, SwingHighEvent):
                self.bos.update_high(swing.swing)

            else:
                self.bos.update_low(swing.swing)

        for e in self.bos.update_candle(event.candle):
            self.bus.publish(e)

    def start(self):
        pass

    def stop(self):
        pass
