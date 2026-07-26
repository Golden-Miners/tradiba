from tradiba.digital_twin.shadow import ShadowOperationEngine

def test_shadow_execution():
    engine = ShadowOperationEngine()
    result = engine.execute_shadow({"price": 100}, {"cash": 1000})
    
    assert result["isolated"] is True
    assert result["simulated_fills"] > 0
