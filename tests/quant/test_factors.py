from tradiba.quant.factors.models import FactorModelingEngine

def test_factors():
    engine = FactorModelingEngine()
    assert engine.calculate_exposure("AAPL", "momentum") == 1.5
