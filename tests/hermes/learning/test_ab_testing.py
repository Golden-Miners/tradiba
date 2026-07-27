from tradiba.hermes.learning.evaluation.ab_testing import ABTestingEngine

def test_ab_testing():
    engine = ABTestingEngine()
    engine.start_experiment("exp_1", "Prompt_A", "Prompt_B")
    
    engine.record_result("exp_1", "a", 90.0)
    engine.record_result("exp_1", "a", 80.0)
    engine.record_result("exp_1", "b", 95.0)
    engine.record_result("exp_1", "b", 95.0)
    
    winner = engine.get_winner("exp_1")
    assert winner == "variant_b"
