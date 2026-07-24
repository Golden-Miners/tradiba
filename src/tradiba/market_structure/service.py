from tradiba.market.events import CandleClosedEvent
from tradiba.core.service import Service

from .state import MarketStructureState
from .detector import SwingDetector
from .bos import BOSDetector
from .choch import CHOCHDetector
from .liquidity import LiquidityDetector

from .events import (
    SwingHighEvent,
    BullishBOSEvent,
    BearishBOSEvent,
    TrendChangedEvent,
    BullishCHOCHEvent,
    BearishCHOCHEvent,
)


class MarketStructureService(Service):

    def __init__(self, event_bus):
        self.bus = event_bus
        
        self.state = MarketStructureState()
        
        self.swing_detector = SwingDetector()
        self.bos = BOSDetector()
        self.choch = CHOCHDetector()
        self.liquidity = LiquidityDetector()

    def on_candle_closed(self, event: CandleClosedEvent):

        # 1. Swing Detection
        swing = self.swing_detector.update(event.candle)
        if swing:
            if isinstance(swing, SwingHighEvent):
                self.state.last_swing_high = swing.swing
            else:
                self.state.last_swing_low = swing.swing
                
            self.bus.publish(swing)

            # Liquidity Creation Detection
            for e in self.liquidity.update_swing(swing.swing, self.state):
                self.bus.publish(e)

        # 2. BOS Detection
        bos_events = self.bos.update_candle(event.candle, self.state)
        for e in bos_events:
            if isinstance(e, BullishBOSEvent):
                self.state.last_broken_high = e.broken_price
            elif isinstance(e, BearishBOSEvent):
                self.state.last_broken_low = e.broken_price
            elif isinstance(e, TrendChangedEvent):
                self.state.trend = e.current
                # Reset CHOCH detection on new trend confirmation
                self.state.choch_detected = False
                
            self.bus.publish(e)

        # 3. CHOCH Detection
        choch_events = self.choch.update(event.candle, self.state)
        for e in choch_events:
            if isinstance(e, BullishCHOCHEvent) or isinstance(e, BearishCHOCHEvent):
                self.state.choch_detected = True
                
            self.bus.publish(e)

        # 4. Liquidity Sweep Detection
        sweep_events = self.liquidity.check_sweep(event.candle, self.state)
        for e in sweep_events:
            self.bus.publish(e)

    def start(self):
        pass

    def stop(self):
        pass
