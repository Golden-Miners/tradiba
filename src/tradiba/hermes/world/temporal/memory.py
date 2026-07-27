from collections import deque
from tradiba.hermes.world.model.world import WorldState

class TemporalMemory:
    """
    Tracks historical evolution of the world state using an in-memory ring buffer.
    """
    def __init__(self, max_history_size: int = 1000):
        self.history: deque[WorldState] = deque(maxlen=max_history_size)
        
    def record_state(self, state: WorldState):
        """
        Record a snapshot of the current state.
        """
        self.history.append(state.clone())
        
    def get_state_at(self, timestamp: float) -> WorldState | None:
        """
        Finds the closest state recorded at or before the given timestamp.
        """
        closest_state = None
        for state in self.history:
            if state.timestamp <= timestamp:
                closest_state = state
            else:
                break
        return closest_state
