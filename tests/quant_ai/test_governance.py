from tradiba.quant_ai.governance.workflow import QuantAIGovernance

def test_governance():
    gov = QuantAIGovernance()
    assert gov.approve_model("m1")
