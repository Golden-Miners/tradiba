from tradiba.quant.governance.workflow import QuantitativeGovernance

def test_governance():
    gov = QuantitativeGovernance()
    assert gov.validate_promotion("m1")
