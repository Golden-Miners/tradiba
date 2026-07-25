from typing import Callable, Any, Type
from tradiba.events.base import Event

def subscribe(event_type: Type[Event]):
    """
    Decorator to mark a plugin method as a subscriber to an event.
    """
    def decorator(func: Callable[[Any, Event], None]):
        func._subscribe_event = event_type  # type: ignore
        return func
    return decorator
