from tradiba.hermes.portfolio.attribution.performance import PerformanceAttribution

def test_attribution_calculation():
    attribution = PerformanceAttribution({})
    port_rets = [0.01, 0.02]
    strat_rets = {
        "s1": [0.02, 0.04],
        "s2": [0.00, 0.00]
    }
    allocs = {
        "s1": [0.5, 0.5],
        "s2": [0.5, 0.5]
    }
    
    result = attribution.calculate_attribution(port_rets, strat_rets, allocs)
    assert result["strategy_contribution"]["s1"] == (0.02*0.5 + 0.04*0.5)
    assert result["strategy_contribution"]["s2"] == (0.00*0.5 + 0.00*0.5)
