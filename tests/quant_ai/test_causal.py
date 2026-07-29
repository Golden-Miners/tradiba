from tradiba.quant_ai.causal.inference import CausalInferenceEngine

def test_causal():
    engine = CausalInferenceEngine()
    assert engine.estimate_treatment_effect("new_algo", "fill_rate") == 1.2
