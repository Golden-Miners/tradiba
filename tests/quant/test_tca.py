from tradiba.quant.tca.engine import TransactionCostAnalysisEngine

def test_tca():
    engine = TransactionCostAnalysisEngine()
    costs = engine.analyze_cost("t1")
    assert costs["slippage"] == 0.01
