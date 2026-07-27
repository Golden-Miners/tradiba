
from tradiba.hermes.world.model.world import WorldState

class ScenarioSimulator:
    """
    Simulates various market and infrastructure conditions on a clone of the WorldState.
    Uses the Digital Twin concept to avoid production impact.
    """
    def __init__(self):
        pass
        
    def run_scenario(self, state: WorldState, scenario_type: str) -> WorldState:
        """
        Run a scenario on the given state and return the resulting simulated state.
        Types: 'bull', 'bear', 'flash_crash', 'broker_outage'
        """
        simulated_state = state.clone()
        
        if scenario_type == 'bull':
            # Simulate positive market movement
            for key in simulated_state.market_state:
                if isinstance(simulated_state.market_state[key], (int, float)):
                    simulated_state.market_state[key] *= 1.10
        elif scenario_type == 'bear':
            # Simulate negative market movement
            for key in simulated_state.market_state:
                if isinstance(simulated_state.market_state[key], (int, float)):
                    simulated_state.market_state[key] *= 0.85
        elif scenario_type == 'flash_crash':
            for key in simulated_state.market_state:
                if isinstance(simulated_state.market_state[key], (int, float)):
                    simulated_state.market_state[key] *= 0.50
        elif scenario_type == 'broker_outage':
            simulated_state.infrastructure_state["broker_status"] = "OFFLINE"
            
        return simulated_state
