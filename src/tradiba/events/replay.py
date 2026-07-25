from typing import Type, TypeVar
from tradiba.events.store import EventStore

T = TypeVar('T')

class ReplayEngine:
    def __init__(self, store: EventStore):
        self.store = store

    def replay(self, aggregate_id: str, aggregate_cls: Type[T]) -> T:
        """
        Reconstructs an aggregate entirely from its event stream.
        Assumes the aggregate has a no-arg constructor (or can be instantiated empty)
        and an `apply(event)` method.
        """
        # Load all events for this aggregate
        events = list(self.store.load(aggregate_id))
        
        if not events:
            return None # Or raise an exception, depending on domain preference
            
        # Instantiate empty aggregate. 
        # For our implementation, we assume aggregates have an __init__ that can be called with no args.
        try:
            aggregate = aggregate_cls()
        except TypeError:
            # Fallback to bypass __init__ for aggregates that require args
            aggregate = object.__new__(aggregate_cls)

        for envelope in events:
            apply_method = getattr(aggregate, "apply", None)
            if apply_method:
                apply_method(envelope.event)
            else:
                raise AttributeError(f"Aggregate {aggregate_cls.__name__} has no apply() method")

        return aggregate
