from datetime import datetime

class OperationalCalendar:
    """Unified calendar for operations."""
    def __init__(self) -> None:
        self._events: list[dict] = []
        
    def add_event(self, title: str, start_time: datetime, end_time: datetime, event_type: str) -> None:
        self._events.append({
            "title": title,
            "start_time": start_time,
            "end_time": end_time,
            "type": event_type
        })
        
    def get_events(self, date: datetime) -> list[dict]:
        return [
            e for e in self._events 
            if e["start_time"].date() <= date.date() <= e["end_time"].date()
        ]
