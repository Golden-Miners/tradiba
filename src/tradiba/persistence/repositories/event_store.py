from abc import ABC, abstractmethod
from typing import List
import json
from sqlalchemy.orm import Session

from tradiba.persistence.models.events import MarketEventModel
from tradiba.events import DomainEvent


class EventStore(ABC):
    @abstractmethod
    def append(self, event: DomainEvent) -> None:
        ...

    @abstractmethod
    def get_events(self, start_time=None, end_time=None) -> List[DomainEvent]:
        ...

class SqlAlchemyEventStore(EventStore):
    def __init__(self, session: Session):
        self.session = session

    def append(self, event: DomainEvent) -> None:
        import dataclasses
        from datetime import datetime
        
        # Serialize the dataclass event using a custom serializer for datetime/decimal if needed
        # We'll do a simple representation here assuming the event has standard types
        event_dict = dataclasses.asdict(event)
        
        # We need a safe JSON serialization
        def default_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            # Add decimal serialization if needed
            from decimal import Decimal
            if isinstance(obj, Decimal):
                return str(obj)
            # Enum
            from enum import Enum
            if isinstance(obj, Enum):
                return obj.value
            raise TypeError(f"Type not serializable: {type(obj)}")
            
        payload = json.dumps(event_dict, default=default_serializer)

        # We assume event might have symbol and timestamp
        symbol = getattr(event, "symbol", "UNKNOWN")
        timestamp = getattr(event, "timestamp", datetime.utcnow())

        model = MarketEventModel(
            event_type=event.__class__.__name__,
            timestamp=timestamp,
            symbol=symbol,
            payload=payload
        )
        self.session.add(model)

    def get_events(self, start_time=None, end_time=None) -> List[DomainEvent]:
        # For a full implementation this would re-instantiate the concrete Event classes
        return []
