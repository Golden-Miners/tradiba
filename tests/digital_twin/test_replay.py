from uuid import uuid4
from tradiba.digital_twin.replay import ReplayEngine

def test_deterministic_replay():
    engine = ReplayEngine()
    
    events = [{"id": 1}, {"id": 2}]
    assert engine.replay_events(uuid4(), events) is True
