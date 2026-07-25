from typing import Type
from tradiba.events.event import DomainEvent

class EventRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, event_type: Type[DomainEvent]) -> None:
        self._registry[event_type.__name__] = event_type

    def resolve(self, name: str) -> Type[DomainEvent]:
        if name not in self._registry:
            raise ValueError(f"Event type {name} not found in registry")
        return self._registry[name]

# Global registry instance
registry = EventRegistry()
