from tradiba.quant.alpha.engine import AlphaResearchEngine

def test_alpha():
    engine = AlphaResearchEngine()
    alpha_id = engine.register_alpha("test", "momentum > 0")
    assert alpha_id == "alpha_0"
    assert len(engine.alphas) == 1
