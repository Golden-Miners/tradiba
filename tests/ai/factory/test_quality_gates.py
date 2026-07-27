from tradiba.ai.factory.governance.quality_gates import AIQualityGates

def test_quality_gates():
    gates = AIQualityGates()
    assert gates.evaluate_gates({"accuracy": 0.95, "hallucination": 0.01, "latency": 100})
    assert not gates.evaluate_gates({"accuracy": 0.80, "hallucination": 0.01, "latency": 100})
