from tradiba.hermes.world.model.world import WorldState
from tradiba.hermes.world.scenarios.simulator import ScenarioSimulator

def test_scenario_simulator():
    simulator = ScenarioSimulator()
    state = WorldState()
    state.market_state["AAPL"] = 100
    
    sim_bull = simulator.run_scenario(state, "bull")
    assert sim_bull.market_state["AAPL"] > 100
    
    sim_bear = simulator.run_scenario(state, "bear")
    assert sim_bear.market_state["AAPL"] < 100
    
    sim_outage = simulator.run_scenario(state, "broker_outage")
    assert sim_outage.infrastructure_state["broker_status"] == "OFFLINE"
    
    # Original state is unmodified
    assert state.market_state["AAPL"] == 100
    assert "broker_status" not in state.infrastructure_state
