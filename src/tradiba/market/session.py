from dataclasses import dataclass
from datetime import time, datetime
from enum import Enum
from tradiba.events import DomainEvent, EventBus
from tradiba.market.events import CandleClosedEvent

class SessionName(Enum):
    SYDNEY = "Sydney"
    TOKYO = "Tokyo"
    LONDON = "London"
    NEW_YORK = "New York"
    UNKNOWN = "Unknown"

@dataclass(slots=True)
class TradingSession:
    name: SessionName
    start_utc: time
    end_utc: time

@dataclass(frozen=True, slots=True)
class SessionOpenedEvent(DomainEvent):
    session: TradingSession
    timestamp: datetime

@dataclass(frozen=True, slots=True)
class SessionClosedEvent(DomainEvent):
    session: TradingSession
    timestamp: datetime


class SessionEngine:
    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus
        self._sessions = [
            TradingSession(name=SessionName.SYDNEY, start_utc=time(22, 0), end_utc=time(7, 0)),
            TradingSession(name=SessionName.TOKYO, start_utc=time(0, 0), end_utc=time(9, 0)),
            TradingSession(name=SessionName.LONDON, start_utc=time(8, 0), end_utc=time(16, 0)),
            TradingSession(name=SessionName.NEW_YORK, start_utc=time(13, 0), end_utc=time(22, 0))
        ]
        self._active_sessions = set()
        
    def start(self):
        self._event_bus.subscribe(CandleClosedEvent, self._on_candle)
        
    def stop(self):
        self._event_bus.unsubscribe(CandleClosedEvent, self._on_candle)

    def get_active_sessions(self) -> set[SessionName]:
        """Return the set of currently active trading sessions."""
        return set(self._active_sessions)

    def is_session_active(self, name: SessionName) -> bool:
        """Check whether a specific session is currently active."""
        return name in self._active_sessions
        
    def _is_in_session(self, t: time, session: TradingSession) -> bool:
        if session.start_utc < session.end_utc:
            return session.start_utc <= t < session.end_utc
        else: # Crosses midnight
            return t >= session.start_utc or t < session.end_utc

    def _on_candle(self, event: CandleClosedEvent):
        # Determine sessions based on candle timestamp
        candle_time = event.candle.timestamp.time()
        
        currently_active = set()
        for s in self._sessions:
            if self._is_in_session(candle_time, s):
                currently_active.add(s.name)
                
        # Find newly opened sessions
        newly_opened = currently_active - self._active_sessions
        for name in newly_opened:
            s = next(x for x in self._sessions if x.name == name)
            self._event_bus.publish(SessionOpenedEvent(session=s, timestamp=event.candle.timestamp))
            
        # Find newly closed sessions
        newly_closed = self._active_sessions - currently_active
        for name in newly_closed:
            s = next(x for x in self._sessions if x.name == name)
            self._event_bus.publish(SessionClosedEvent(session=s, timestamp=event.candle.timestamp))
            
        self._active_sessions = currently_active
