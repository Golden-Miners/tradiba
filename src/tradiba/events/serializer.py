from abc import ABC, abstractmethod
import json
import dataclasses
from uuid import UUID
from datetime import datetime
from enum import Enum
from decimal import Decimal

from tradiba.events.envelope import EventEnvelope
from tradiba.events.registry import registry

class EventSerializer(ABC):
    @abstractmethod
    def serialize(self, envelope: EventEnvelope) -> bytes:
        ...

    @abstractmethod
    def deserialize(self, payload: bytes) -> EventEnvelope:
        ...

class JsonEventSerializer(EventSerializer):
    def serialize(self, envelope: EventEnvelope) -> bytes:
        def default_serializer(obj):
            if isinstance(obj, UUID):
                return str(obj)
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, Decimal):
                return str(obj)
            if isinstance(obj, Enum):
                return obj.value
            if dataclasses.is_dataclass(obj):
                return dataclasses.asdict(obj)
            raise TypeError(f"Type not serializable: {type(obj)}")

        data = {
            "aggregate_id": envelope.aggregate_id,
            "aggregate_type": envelope.aggregate_type,
            "sequence": envelope.sequence,
            "correlation_id": envelope.correlation_id,
            "causation_id": envelope.causation_id,
            "event_type": envelope.event.__class__.__name__,
            "event_payload": dataclasses.asdict(envelope.event)
        }
        return json.dumps(data, default=default_serializer).encode("utf-8")

    def deserialize(self, payload: bytes) -> EventEnvelope:
        data = json.loads(payload.decode("utf-8"))
        
        event_cls = registry.resolve(data["event_type"])
        event_payload = data["event_payload"]
        
        # We need a robust mechanism to construct the event from the payload, handling nested objects, datetimes and UUIDs.
        # For simplicity, we assume the event class kwargs align with the payload, and we do minimal conversion here.
        # A full implementation would introspect type hints to cast properly.
        if "event_id" in event_payload and isinstance(event_payload["event_id"], str):
            event_payload["event_id"] = UUID(event_payload["event_id"])
        if "occurred_at" in event_payload and isinstance(event_payload["occurred_at"], str):
            event_payload["occurred_at"] = datetime.fromisoformat(event_payload["occurred_at"])

        event = event_cls(**event_payload)

        return EventEnvelope(
            aggregate_id=data["aggregate_id"],
            aggregate_type=data["aggregate_type"],
            sequence=data["sequence"],
            correlation_id=data.get("correlation_id"),
            causation_id=data.get("causation_id"),
            event=event
        )
