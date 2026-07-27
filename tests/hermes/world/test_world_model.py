from tradiba.hermes.world.model.world import WorldModelBuilder

def test_world_model_updates():
    builder = WorldModelBuilder()
    
    builder.update_market({"BTC": 50000})
    state = builder.get_state()
    assert state.market_state["BTC"] == 50000
    
    builder.update_portfolio({"exposure": 0.5})
    state2 = builder.get_state()
    assert state2.portfolio_state["exposure"] == 0.5
    
    # Check isolation (cloning works)
    assert "exposure" not in state.portfolio_state
