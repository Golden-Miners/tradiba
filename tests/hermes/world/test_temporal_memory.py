import time
from tradiba.hermes.world.model.world import WorldState
from tradiba.hermes.world.temporal.memory import TemporalMemory

def test_temporal_memory_records_and_retrieves():
    memory = TemporalMemory(max_history_size=5)
    
    state1 = WorldState()
    state1.market_state["AAPL"] = 150
    memory.record_state(state1)
    
    time.sleep(0.01)
    t1 = time.time()
    time.sleep(0.01)
    
    state2 = WorldState()
    state2.market_state["AAPL"] = 155
    memory.record_state(state2)
    
    retrieved = memory.get_state_at(t1)
    assert retrieved is not None
    assert retrieved.market_state["AAPL"] == 150
