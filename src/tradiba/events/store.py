from abc import ABC, abstractmethod
from typing import List, Generator, Optional
import json

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from tradiba.events.envelope import EventEnvelope
from tradiba.events.serializer import EventSerializer, JsonEventSerializer
from tradiba.events.exceptions import ConcurrencyException
from tradiba.persistence.models.event_store import StoredEventModel

class EventStore(ABC):
    @abstractmethod
    def append(self, envelope: EventEnvelope) -> None:
        ...

    @abstractmethod
    def append_batch(self, envelopes: List[EventEnvelope]) -> None:
        ...

    @abstractmethod
    def load(self, aggregate_id: str, after_sequence: int = 0) -> Generator[EventEnvelope, None, None]:
        ...

class SqlAlchemyEventStore(EventStore):
    def __init__(self, session: Session, serializer: Optional[EventSerializer] = None):
        self.session = session
        self.serializer = serializer or JsonEventSerializer()

    def append(self, envelope: EventEnvelope) -> None:
        self.append_batch([envelope])

    def append_batch(self, envelopes: List[EventEnvelope]) -> None:
        models = []
        for envelope in envelopes:
            serialized_payload = self.serializer.serialize(envelope)
            # The serializer returns a JSON string encoded as bytes. We decode it to store in JSON column directly.
            payload_dict = json.loads(serialized_payload.decode('utf-8'))
            
            # Since the payload already contains the envelope metadata, we can just store it in the JSON column,
            # or separate it out.
            model = StoredEventModel(
                event_id=str(envelope.event.event_id),
                aggregate_id=envelope.aggregate_id,
                aggregate_type=envelope.aggregate_type,
                sequence=envelope.sequence,
                event_type=envelope.event.__class__.__name__,
                event_version=envelope.event.version,
                occurred_at=envelope.event.occurred_at,
                payload=payload_dict
            )
            models.append(model)

        self.session.add_all(models)
        try:
            self.session.flush() # Flush to catch integrity errors early (e.g., sequence collision)
        except IntegrityError as e:
            raise ConcurrencyException(f"Concurrency error appending events: {e}") from e

    def load(self, aggregate_id: str, after_sequence: int = 0) -> Generator[EventEnvelope, None, None]:
        query = self.session.query(StoredEventModel) \
            .filter(StoredEventModel.aggregate_id == aggregate_id) \
            .filter(StoredEventModel.sequence > after_sequence) \
            .order_by(StoredEventModel.sequence.asc())
        
        for model in query.all():
            # encode the dictionary back to bytes to satisfy the serializer interface
            payload_bytes = json.dumps(model.payload).encode('utf-8')
            envelope = self.serializer.deserialize(payload_bytes)
            yield envelope
