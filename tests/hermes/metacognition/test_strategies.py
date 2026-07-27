from tradiba.hermes.metacognition.strategies.adaptive_strategies import AdaptiveReasoningStrategies

def test_strategies():
    strats = AdaptiveReasoningStrategies()
    assert strats.select_strategy("NORMAL", "HIGH") == "fast_heuristic"
    assert strats.select_strategy("PORTFOLIO_ROTATION", "NORMAL") == "deep_analytical"
    assert strats.select_strategy("EMERGENCY_EXIT", "NORMAL") == "risk_first"
