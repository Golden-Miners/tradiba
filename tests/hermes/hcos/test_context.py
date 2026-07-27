from tradiba.hermes.hcos.context.engine import ContextEngine

def test_context_engine():
    engine = ContextEngine()
    state = {"market": "bull", "portfolio": "high_risk", "irrelevant": "yes"}
    res = engine.build_context(state, ["market"])
    assert res == {"market": "bull"}
    assert "irrelevant" not in res
