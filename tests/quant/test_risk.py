from tradiba.quant.risk.models import QuantitativeRiskModels

def test_risk():
    models = QuantitativeRiskModels()
    assert models.calculate_var("portfolio_1") == 0.05
