from typing import Dict, Any, List
import copy
from datetime import datetime

class WorldState:
    """
    Represents a snapshot of the entire trading ecosystem.
    """
    def __init__(self):
        self.market_state: Dict[str, Any] = {}
        self.portfolio_state: Dict[str, Any] = {}
        self.infrastructure_state: Dict[str, Any] = {}
        self.macro_events: List[Dict[str, Any]] = []
        self.timestamp: float = datetime.now().timestamp()
        
    def clone(self) -> 'WorldState':
        """Deep copy the state for simulations."""
        new_state = WorldState()
        new_state.market_state = copy.deepcopy(self.market_state)
        new_state.portfolio_state = copy.deepcopy(self.portfolio_state)
        new_state.infrastructure_state = copy.deepcopy(self.infrastructure_state)
        new_state.macro_events = copy.deepcopy(self.macro_events)
        new_state.timestamp = self.timestamp
        return new_state


class WorldModelBuilder:
    """
    Listens to live platform events and continuously updates the WorldState.
    """
    def __init__(self):
        self.current_state = WorldState()
        
    def update_market(self, updates: Dict[str, Any]):
        self.current_state.market_state.update(updates)
        self.current_state.timestamp = datetime.now().timestamp()
        
    def update_portfolio(self, updates: Dict[str, Any]):
        self.current_state.portfolio_state.update(updates)
        self.current_state.timestamp = datetime.now().timestamp()
        
    def get_state(self) -> WorldState:
        return self.current_state.clone()
