import pytest
from uuid import uuid4
from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tradiba.persistence.models import Base
from tradiba.events.store import SqlAlchemyEventStore
from tradiba.events.envelope import EventEnvelope
from tradiba.events.event import DomainEvent
from tradiba.events.registry import registry
from tradiba.events.replay import ReplayEngine

@dataclass(slots=True, frozen=True)
class CounterIncrementedEvent(DomainEvent):
    amount: int

@dataclass(slots=True, frozen=True)
class CounterResetEvent(DomainEvent):
    pass

registry.register(CounterIncrementedEvent)
registry.register(CounterResetEvent)

class CounterAggregate:
    def __init__(self):
        self.count = 0

    def apply(self, event):
        handler = getattr(self, f"_apply_{event.__class__.__name__}", None)
        if handler:
            handler(event)

    def _apply_CounterIncrementedEvent(self, event: CounterIncrementedEvent):
        self.count += event.amount

    def _apply_CounterResetEvent(self, event: CounterResetEvent):
        self.count = 0

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_replay_aggregate(session):
    store = SqlAlchemyEventStore(session)
    engine = ReplayEngine(store)
    
    aggregate_id = str(uuid4())
    
    events = [
        EventEnvelope(aggregate_id=aggregate_id, aggregate_type="Counter", sequence=1, event=CounterIncrementedEvent.create(amount=5)),
        EventEnvelope(aggregate_id=aggregate_id, aggregate_type="Counter", sequence=2, event=CounterIncrementedEvent.create(amount=10)),
        EventEnvelope(aggregate_id=aggregate_id, aggregate_type="Counter", sequence=3, event=CounterResetEvent.create()),
        EventEnvelope(aggregate_id=aggregate_id, aggregate_type="Counter", sequence=4, event=CounterIncrementedEvent.create(amount=3)),
    ]
    
    store.append_batch(events)
    
    # Replay
    aggregate = engine.replay(aggregate_id, CounterAggregate)
    
    assert aggregate is not None
    assert aggregate.count == 3
