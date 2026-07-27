from tradiba.hermes.scientist.hypotheses.engine import HypothesisEngine

def test_hypotheses():
    engine = HypothesisEngine()
    h = engine.generate_hypothesis("h1", "x increases")
    assert "If x increases" in h
